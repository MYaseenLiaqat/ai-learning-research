"""Python grading service.

Runs submitted code in a subprocess with hidden tests.

SECURITY LIMITATION
-------------------
The current grader uses `python -I` in a temporary directory. This provides
basic isolation (ignores PYTHONPATH, runs in a fresh temp dir) but does NOT
provide true network or OS-level sandboxing. Submitted code can still make
network calls, access the filesystem, or consume resources.

Current grader is acceptable only for a controlled/internal technical pilot
with trusted participants. Real untrusted/public code execution requires
stronger OS/container/VM sandboxing.
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

TIMEOUT_SECONDS = 4

def grade_python(code: str, grading_spec: dict):
    tests = grading_spec.get("tests", [])
    if not tests:
        return 0.0, ["No tests configured."]

    passed = 0
    feedback = []

    with tempfile.TemporaryDirectory() as td:
        submission = Path(td) / "submission.py"
        submission.write_text(code, encoding="utf-8")

        for i, test in enumerate(tests, 1):
            harness = f'''
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from submission import *

try:
    result = ({test["expression"]})
    expected = {test["expected"]!r}
    print(json.dumps({{"ok": result == expected}}))
except Exception as exc:
    print(json.dumps({{"ok": False, "error": str(exc)}}))
'''
            hp = Path(td) / f"harness_{i}.py"
            hp.write_text(harness, encoding="utf-8")
            try:
                proc = subprocess.run(
                    [sys.executable, "-I", str(hp)],
                    cwd=td,
                    capture_output=True,
                    text=True,
                    timeout=TIMEOUT_SECONDS,
                    env={"PYTHONPATH": td, "PYTHONIOENCODING": "utf-8"},
                )
                data = json.loads(proc.stdout.strip().splitlines()[-1])
                if data.get("ok"):
                    passed += 1
                    feedback.append(f"Test {i}: passed")
                else:
                    feedback.append(f"Test {i}: failed")
            except subprocess.TimeoutExpired:
                feedback.append(f"Test {i}: timeout")
            except Exception as exc:
                feedback.append(f"Test {i}: execution error ({exc})")

    return round(passed / len(tests), 4), feedback
