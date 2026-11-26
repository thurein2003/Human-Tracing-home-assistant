"""Run a reviewed controller as a loopback-only Flask development server."""
import os
from pathlib import Path
import runpy

from flask import Flask

PORT = int(os.environ.get("EYETRACE_PI_WEB_PORT", "8080"))
if not 1 <= PORT <= 65535:
    raise ValueError("Invalid dashboard port")

original_run = Flask.run


def run_on_loopback(self, host=None, port=None, debug=None, load_dotenv=True, **options):
    options.update(use_reloader=False, use_debugger=False)
    return original_run(self, host="127.0.0.1", port=PORT, debug=False,
                        load_dotenv=False, **options)


if __name__ == "__main__":
    Flask.run = run_on_loopback
    runpy.run_path(str(Path(__file__).with_name("manual_web.py")), run_name="__main__")
