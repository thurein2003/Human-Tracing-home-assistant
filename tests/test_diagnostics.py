import importlib.util
import json
from decimal import Decimal
from pathlib import Path
import unittest
from unittest.mock import MagicMock, patch
from urllib.error import URLError

PI = Path(__file__).resolve().parents[1] / "software" / "raspberry-pi"


def load(filename):
    spec = importlib.util.spec_from_file_location(filename.replace("-", "_"), PI / (filename + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ollama = load("ollama-test")
calibration = load("calibration-plan")
OBSERVATION = dict(person_visible=True, possible_person=True, horizontal="center",
                   vertical="center", action="follow", confidence=0.8, reason="Visible", speech="")


class ObservationTests(unittest.TestCase):
    def test_accepts_historical_response_shape(self):
        self.assertEqual(ollama.validate_observation(OBSERVATION), OBSERVATION)

    def test_rejects_missing_and_extra_fields(self):
        missing = OBSERVATION.copy()
        del missing["speech"]
        for value in (None, [], missing, dict(OBSERVATION, unknown=False)):
            with self.subTest(value=value), self.assertRaises(ValueError):
                ollama.validate_observation(value)

    def test_rejects_invalid_values(self):
        for key, values in {"confidence": [True, 1.1, -0.1, float("nan"), float("inf"), "0.8"],
                            "action": [None, "x" * 1025], "person_visible": ["true", 1],
                            "horizontal": ["above", []], "vertical": ["left", None]}.items():
            for value in values:
                with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                    ollama.validate_observation(dict(OBSERVATION, **{key: value}))

    def test_network_error_and_timeout(self):
        for error in (URLError("offline"), TimeoutError("slow")):
            opener = MagicMock()
            opener.open.side_effect = error
            with (self.subTest(error=error),
                  patch.object(ollama, "build_opener", return_value=opener),
                  self.assertRaises(ConnectionError)):
                ollama.query(11435, "tags", timeout=2)
            request = opener.open.call_args.args[0]
            self.assertEqual(request.full_url, "http://127.0.0.1:11435/api/tags")
            self.assertEqual(opener.open.call_args.kwargs["timeout"], 2)

    def test_invalid_json(self):
        opener = MagicMock()
        opener.open.return_value.__enter__.return_value.read.return_value = b"bad response"
        with patch.object(ollama, "build_opener", return_value=opener):
            with self.assertRaises(json.JSONDecodeError):
                ollama.query(11435, "tags")

    def test_invalid_configuration_before_network(self):
        with patch.object(ollama, "build_opener") as opener:
            for port, timeout in ((0, 5), (65536, 5), (11435, 0)):
                with self.subTest(port=port, timeout=timeout), self.assertRaises(ValueError):
                    ollama.query(port, "tags", timeout=timeout)
            opener.assert_not_called()


class CalibrationTests(unittest.TestCase):
    def test_bounds_step_and_return_to_neutral(self):
        low, neutral, high, step = map(Decimal, ("85", "90", "95", "1.5"))
        positions = calibration.plan(low, neutral, high, step)
        self.assertEqual((min(positions), max(positions)), (low, high))
        self.assertEqual((positions[0], positions[-1]), (neutral, neutral))
        self.assertTrue(all(abs(a-b) <= step for a, b in zip(positions, positions[1:])))

    def test_rejects_unsafe_or_non_finite_plan(self):
        for args in (("0", "90", "180", "1"), ("-1", "90", "95", "1"), ("91", "90", "95", "1"),
                     ("85", "90", "95", "6"), ("85", "NaN", "95", "1"), ("85", "90", "95", "0")):
            with self.subTest(args=args), self.assertRaises(ValueError):
                calibration.plan(*map(Decimal, args))


class DeploymentTests(unittest.TestCase):
    def test_example_configuration_names_and_ports(self):
        config = PI.parents[1] / "config" / "eyetrace.env.example"
        values = dict(line.split("=", 1) for line in config.read_text(encoding="utf-8").splitlines() if line)
        self.assertEqual(values.pop("EYETRACE_SSH_TARGET"), "pi-user@pi-host")
        self.assertEqual(values.pop("EYETRACE_MODEL"), "gemma3:4b")
        self.assertEqual(len(values), 4)
        self.assertTrue(all(key.endswith("_PORT") and 1 <= int(port) <= 65535
                            for key, port in values.items()))
    def test_launcher_forces_loopback_and_disables_debug(self):
        import sys
        flask = MagicMock()
        with patch.dict(sys.modules, {"flask": flask}), patch.dict("os.environ", {"EYETRACE_PI_WEB_PORT": "8082"}):
            launcher = load("launch_dashboard")
            app = object()
            launcher.run_on_loopback(app, host="0.0.0.0", port=80, debug=True, use_reloader=True)
            flask.Flask.run.assert_called_once_with(
                app, host="127.0.0.1", port=8082, debug=False, load_dotenv=False,
                use_reloader=False, use_debugger=False)

    def test_launcher_rejects_invalid_port(self):
        import sys
        with patch.dict(sys.modules, {"flask": MagicMock()}), patch.dict("os.environ", {"EYETRACE_PI_WEB_PORT": "65536"}):
            with self.assertRaises(ValueError):
                load("launch_dashboard")


if __name__ == "__main__":
    unittest.main()
