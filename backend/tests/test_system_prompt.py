from app.routers.ai import (
    SYSTEM_PROMPT,
    SYSTEM_PROMPT_REGISTRY,
    SYSTEM_PROMPT_VERSION,
    get_system_prompt,
)


def test_system_prompt_version_is_030_and_020_remains_resolvable():
    assert SYSTEM_PROMPT_VERSION == "0.3.0"
    assert get_system_prompt("0.2.0") == SYSTEM_PROMPT_REGISTRY["0.2.0"]
    assert get_system_prompt("0.3.0") == SYSTEM_PROMPT


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
        "while loops",
        "nested loops",
        "break",
        "continue",
        "functions",
        "recursion",
        "dictionaries",
        "comprehensions",
        "advanced libraries",
        "other solution shortcuts outside the learning construct",
    ]:
        assert term in SYSTEM_PROMPT


def test_system_prompt_forbids_complete_active_task_solution():
    assert "complete solution" in SYSTEM_PROMPT
    assert "Do not provide the complete active-task solution" in SYSTEM_PROMPT


def test_system_prompt_allows_concepts_hints_tracing_and_analogies():
    for term in [
        "Answer conceptual questions clearly and directly",
        "targeted hints",
        "tracing",
        "dry-run reasoning",
        "analogous examples using different variables, values, or context",
    ]:
        assert term in SYSTEM_PROMPT


def test_system_prompt_does_not_redefine_provided_inputs():
    assert "Do not redefine a provided input" in SYSTEM_PROMPT
    assert "operate on the input variables exactly as\nprovided by the platform" in SYSTEM_PROMPT


def test_system_prompt_keeps_fixed_tutoring_policy():
    assert "same tutoring policy for every participant" in SYSTEM_PROMPT
    assert "Do not reveal hidden tests" in SYSTEM_PROMPT
    assert "Do not reveal research hypotheses" in SYSTEM_PROMPT
    assert "Do not personalize the experimental treatment" in SYSTEM_PROMPT
    assert "Do not use cross-task memory" in SYSTEM_PROMPT