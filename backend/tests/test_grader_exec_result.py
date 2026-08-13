from app.services.grader import grade_python


def test_exec_result_normal_case():
    code = (
        "result = 0\n"
        "for t in temperatures:\n"
        "    if t > 30:\n"
        "        result += 1\n"
    )
    spec = {
        "mode": "exec_result",
        "result_var": "result",
        "tests": [
            {"inputs": {"temperatures": [28, 32, 35, 29, 31, 27]}, "expected": 3},
        ],
    }
    score, _ = grade_python(code, spec)
    assert score == 1.0


def test_exec_result_boundary_case():
    code = (
        "result = 0\n"
        "for t in temperatures:\n"
        "    if t > 30:\n"
        "        result += 1\n"
    )
    spec = {
        "mode": "exec_result",
        "result_var": "result",
        "tests": [
            {"inputs": {"temperatures": [30, 30]}, "expected": 0},
            {"inputs": {"temperatures": [31, 31]}, "expected": 2},
        ],
    }
    score, _ = grade_python(code, spec)
    assert score == 1.0


def test_exec_result_list_result_case():
    code = (
        "result = []\n"
        "for t in temperatures:\n"
        "    if t > 30:\n"
        "        result.append(t)\n"
    )
    spec = {
        "mode": "exec_result",
        "result_var": "result",
        "tests": [
            {"inputs": {"temperatures": [25, 34, 29, 41, 31]}, "expected": [34, 41, 31]},
        ],
    }
    score, _ = grade_python(code, spec)
    assert score == 1.0


def test_exec_result_fresh_namespace_per_case():
    """State must not leak between hidden test cases."""
    # A buggy solution that mutates the input list would fail on a later case
    # if the namespace were shared. With a fresh namespace per case, it passes.
    code = (
        "result = 0\n"
        "for t in temperatures:\n"
        "    if t > 30:\n"
        "        result += 1\n"
    )
    spec = {
        "mode": "exec_result",
        "result_var": "result",
        "tests": [
            {"inputs": {"temperatures": [28, 32, 35]}, "expected": 2},
            {"inputs": {"temperatures": [10, 20]}, "expected": 0},
        ],
    }
    score, _ = grade_python(code, spec)
    assert score == 1.0


def test_exec_result_incorrect_code():
    code = "result = 0\n"
    spec = {
        "mode": "exec_result",
        "result_var": "result",
        "tests": [
            {"inputs": {"temperatures": [28, 32, 35]}, "expected": 2},
        ],
    }
    score, _ = grade_python(code, spec)
    assert score == 0.0