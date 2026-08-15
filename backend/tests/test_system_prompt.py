from app.routers.ai import SYSTEM_PROMPT, SYSTEM_PROMPT_VERSION


def test_system_prompt_version_is_020():
    assert SYSTEM_PROMPT_VERSION == "0.2.0"


def test_system_prompt_permits_loop_constructs():
    for term in [
        "for loops",
        "if statements",
        "comparison operators",
        "counters and accumulators",
        "the result variable",
        "variables",
        "assignment",
    ]:
        assert term in SYSTEM_PROMPT


def test_system_prompt_forbids_out_of_construct_solutions():
    for term in [
        "list comprehensions",
        "while loops",
        "nested loops",
        "break",
        "continue",
        "functions as the solution abstraction",
        "recursion",
        "dictionaries",
        "advanced libraries",
        "bypasses the for-loop construct",
    ]:
        assert term in SYSTEM_PROMPT


def test_system_prompt_allows_complete_solution_within_construct():
    assert "complete solution" in SYSTEM_PROMPT
    assert "must\nuse only the permitted constructs above" in SYSTEM_PROMPT


def test_system_prompt_does_not_redefine_provided_inputs():
    assert "Do not redefine a provided input" in SYSTEM_PROMPT
    assert "operate on the input variables exactly as\nprovided by the platform" in SYSTEM_PROMPT


def test_system_prompt_keeps_fixed_tutoring_policy():
    assert "same tutoring policy for every participant" in SYSTEM_PROMPT
    assert "Do not reveal hidden tests" in SYSTEM_PROMPT
    assert "Do not reveal research hypotheses" in SYSTEM_PROMPT
    assert "Do not personalize the experimental treatment" in SYSTEM_PROMPT
    assert "Do not use cross-task memory" in SYSTEM_PROMPT