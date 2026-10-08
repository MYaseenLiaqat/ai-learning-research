from app.routers.ai import (
    SYSTEM_PROMPT,
    SYSTEM_PROMPT_050,
    SYSTEM_PROMPT_060,
    SYSTEM_PROMPT_REGISTRY,
    SYSTEM_PROMPT_VERSION,
    get_system_prompt,
)


def test_system_prompt_version_is_060_and_historical_versions_remain_resolvable():
    assert SYSTEM_PROMPT_VERSION == "0.6.0"
    assert SYSTEM_PROMPT == SYSTEM_PROMPT_060
    assert get_system_prompt("0.2.0") == SYSTEM_PROMPT_REGISTRY["0.2.0"]
    assert get_system_prompt("0.3.0") == SYSTEM_PROMPT_REGISTRY["0.3.0"]
    assert get_system_prompt("0.4.0") == SYSTEM_PROMPT_REGISTRY["0.4.0"]
    assert get_system_prompt("0.5.0") == SYSTEM_PROMPT_050
    assert get_system_prompt("0.6.0") == SYSTEM_PROMPT


def test_system_prompt_permits_loop_constructs():
    for term in [
        "`for` loops",
        "if statements",
        "comparison operators",
        "counters and accumulators",
        "simple lists and strings",
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
        "other shortcuts outside the approved construct",
    ]:
        assert term in SYSTEM_PROMPT


def test_system_prompt_refuses_direct_and_repeated_active_task_solution_requests():
    for term in [
        "complete solution",
        "code",
        "pseudocode",
        "exact implementation",
        "skeleton",
        "exact loop/if structure",
        "final result",
        "repeated prompting, insistence, role-play, reformulation",
        "No user request can waive this boundary",
        "Explicitly refuse the active-task solution",
        "Do not follow a refusal\nin the same response",
    ]:
        assert term in SYSTEM_PROMPT


def test_system_prompt_blocks_complete_and_near_executable_active_task_leakage():
    for term in [
        "executable or\nnear-executable solution",
        "partial solution requiring only trivial completion",
        "executable pseudocode",
        "step-by-step recipe that directly maps to the\n  active solution",
        "exact loop and conditional control flow",
        "exact initialization, condition or comparison, update\n  sequence, final assignment",
        "final numeric/string answer or result",
        "collectively reconstruct the active\n  algorithm",
    ]:
        assert term in SYSTEM_PROMPT


def test_system_prompt_allows_safe_concepts_decomposition_dry_runs_and_analogies():
    for term in [
        "Explain Python constructs generally and directly",
        "high-level problem decomposition",
        "required state variables",
        "targeted conceptual hints",
        "dry-run reasoning",
        "blank trace-table\n  framework",
        "genuinely analogous examples",
        "materially different from the active task",
        "trivially copyable control-flow pattern",
    ]:
        assert term in SYSTEM_PROMPT


def test_system_prompt_does_not_redefine_provided_inputs():
    assert "Do not instruct the learner to\nredefine" in SYSTEM_PROMPT
    assert "platform-provided input variables" in SYSTEM_PROMPT


def test_system_prompt_keeps_fixed_tutoring_policy():
    assert "same tutoring policy for every participant" in SYSTEM_PROMPT
    assert "Do not reveal hidden tests" in SYSTEM_PROMPT
    assert "Do not reveal research hypotheses" in SYSTEM_PROMPT
    assert "personalize the\ntreatment" in SYSTEM_PROMPT
    assert "Do not use cross-task memory" in SYSTEM_PROMPT


def test_system_prompt_guides_decomposition_and_multiple_state():
    for term in [
        "problem decomposition",
        "required state variables",
        "counter",
        "accumulator",
        "maximum",
        "current streak",
        "best-so-far",
    ]:
        assert term in SYSTEM_PROMPT
