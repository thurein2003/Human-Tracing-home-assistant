"""Check forwarded Ollama model availability and optionally validate a JSON response."""
import argparse
import json
import math
import os
from urllib.error import URLError
from urllib.request import ProxyHandler, build_opener, Request

DIRECTIONS = {"horizontal": {"left", "center", "right"},
              "vertical": {"up", "center", "down"}}
REQUIRED = {"person_visible", "possible_person", "horizontal", "vertical",
            "action", "confidence", "reason", "speech"}


def validate_observation(value):
    if not isinstance(value, dict) or value.keys() != REQUIRED:
        raise ValueError("Unexpected observation fields")
    for field in ("person_visible", "possible_person"):
        if type(value[field]) is not bool:
            raise ValueError(f"Expected boolean {field}")
    for field, allowed in DIRECTIONS.items():
        if not isinstance(value[field], str) or value[field] not in allowed:
            raise ValueError(f"Invalid direction {field}")
    for field in ("action", "reason", "speech"):
        if not isinstance(value[field], str) or len(value[field]) > 1024:
            raise ValueError(f"Invalid text field {field}")
    confidence = value["confidence"]
    if type(confidence) not in (int, float) or not 0 <= confidence <= 1 or not math.isfinite(confidence):
        raise ValueError("Invalid confidence")
    return value


def query(port, route, body=None, timeout=10):
    if not 1 <= port <= 65535 or timeout <= 0:
        raise ValueError("Invalid port or timeout")
    data = None if body is None else json.dumps(body).encode()
    request = Request(f"http://127.0.0.1:{port}/api/{route}", data,
                      headers={"Content-Type": "application/json"})
    try:
        with build_opener(ProxyHandler({})).open(request, timeout=timeout) as response:
            return json.load(response)
    except (URLError, TimeoutError) as error:
        raise ConnectionError(f"Ollama request failed: {error}") from error


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--structured", action="store_true")
    args = parser.parse_args()
    model = os.environ.get("EYETRACE_MODEL", "gemma3:4b")
    try:
        port = int(os.environ.get("EYETRACE_PI_OLLAMA_PORT", "11435"))
        models = query(port, "tags")["models"]
        if not any(entry.get("name") == model for entry in models):
            raise ValueError(f"Missing model {model}")
        print(f"Forwarded Ollama found {model}")
        if args.structured:
            prompt = (
                "This is a diagnostics call. Return a JSON object for an empty scene with "
                "person_visible=false, possible_person=false, horizontal=center, vertical=center, "
                "action=observe, confidence=0.5, reason=Empty scene, speech=empty string."
            )
            result = query(port, "generate", {"model": model, "prompt": prompt, "format": "json",
                           "stream": False}, timeout=90)
            print(json.dumps(validate_observation(json.loads(result["response"]))))
    except (ValueError, ConnectionError, KeyError, TypeError) as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    main()
