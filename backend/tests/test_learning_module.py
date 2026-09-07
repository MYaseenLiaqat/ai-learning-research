def test_learning_module_retrieval(client, make_learner):
    learner = make_learner()
    resp = client.get(f"/learning/loops?learner_id={learner.id}")

    assert resp.status_code == 200
    data = resp.json()
    assert data["module_id"] == "loops"
    assert data["version"] == "v0.4.0"
    assert "explanation" in data
    assert "worked_example" in data
    assert "guided_practice" in data
    assert "static_hints" in data
    assert len(data["static_hints"]) == 3


def test_learning_material_identical_across_conditions(client, make_learner):
    # Both conditions call the same unauthenticated, condition-independent endpoint.
    ai = make_learner(condition="controlled_ai")
    no_ai = make_learner(condition="no_ai")
    ai_resp = client.get(f"/learning/loops?learner_id={ai.id}")
    no_ai_resp = client.get(f"/learning/loops?learner_id={no_ai.id}")

    assert ai_resp.status_code == 200
    assert no_ai_resp.status_code == 200
    # Identical material content for both conditions.
    assert ai_resp.json() == no_ai_resp.json()


def test_guided_practice_is_scaffolded(client, make_learner):
    learner = make_learner()
    resp = client.get(f"/learning/loops?learner_id={learner.id}")
    content = resp.json()["guided_practice"]["problem"]

    assert "___" in content
    assert "for value in stock_levels" in content
    assert "if value" in content
    assert "result" in content


def test_new_lessons_and_practice_are_instructional(client, make_learner):
    content = client.get(f"/learning/loops?learner_id={make_learner().id}").json()
    explanation = content["explanation"]
    assert explanation.count("# Lesson") == 3
    assert "Dry run" in explanation
    assert "result += 1" in explanation
    assert "result += price" in explanation
    assert "mini_practice" in content


def test_learning_module_keeps_historical_versions():
    from app.services.learning_material import get_learning_module

    assert get_learning_module("v0.2.0")["version"] == "v0.2.0"
    assert get_learning_module("v0.3.0")["version"] == "v0.3.0"
    assert get_learning_module("v0.4.0")["version"] == "v0.4.0"


def test_learning_content_stays_within_allowed_constructs():
    from app.services.learning_material import get_learning_module

    content = get_learning_module("v0.4.0")["explanation"].lower()
    forbidden = [
        "range(", "enumerate(", "break", "continue", "pass", "nested",
        "list comprehension", "dictionary", "function", "recursion", "library",
        "append(",
    ]
    assert not any(term in content for term in forbidden)


def test_frontend_material_renderer_uses_safe_dom_operations():
    from pathlib import Path

    source = (Path(__file__).parents[2] / "frontend" / "app.js").read_text()
    renderer = source.split("function appendBasicMarkdown", 1)[1].split(
        "// ---- Rendering: learning material ----", 1
    )[0]
    assert "textContent" in renderer
    assert "createElement(\"table\")" in renderer
    assert "innerHTML" not in renderer


def test_get_learning_loops_does_not_start_session(
    client, db_session, make_learner, make_task, make_attempt
):
    learner = make_learner(condition="controlled_ai")
    task = make_task("supported")
    attempt = make_attempt(learner, task)

    resp = client.get(f"/learning/loops?learner_id={learner.id}")

    assert resp.status_code == 200
    db_session.refresh(attempt)
    assert attempt.started_at is None


def test_task_listing_does_not_start_session(
    client, db_session, make_learner, make_task, make_attempt
):
    learner = make_learner(condition="controlled_ai")
    task = make_task("supported")
    attempt = make_attempt(learner, task)

    resp = client.get(f"/tasks/learner/{learner.id}")

    assert resp.status_code == 200
    db_session.refresh(attempt)
    assert attempt.started_at is None