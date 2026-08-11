from app.services.grader import grade_python

def test_correct_code():
    score, _ = grade_python(
        "def add(a,b):\n    return a+b\n",
        {"tests": [
            {"expression": "add(1,2)", "expected": 3},
            {"expression": "add(-1,5)", "expected": 4},
        ]},
    )
    assert score == 1.0

def test_incorrect_code():
    score, _ = grade_python(
        "def add(a,b):\n    return a-b\n",
        {"tests": [{"expression": "add(1,2)", "expected": 3}]},
    )
    assert score == 0.0
