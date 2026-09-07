from datetime import datetime, timedelta
from unittest.mock import patch

from app.config import settings
from app.models import AIInteraction, Attempt
from app.routers.ai import SYSTEM_PROMPT_REGISTRY, SYSTEM_PROMPT_VERSION
from app.services.learning_material import MODULE_REGISTRY
from app.services.grader import GRADER_VERSION


def configure_llm(monkeypatch):
    monkeypatch.setattr(settings, "llm_base_url", "http://fake-llm")
    monkeypatch.setattr(settings, "llm_api_key", "fake-key")


def fake_response():
    class Response:
        def raise_for_status(self):
            pass

        def json(self):
            return {"choices": [{"message": {"content": "answer"}}]}

    return Response()


def test_new_learner_freezes_provenance(client, db_session, monkeypatch):
    monkeypatch.setattr(settings, "llm_model", "frozen-model")
    response = client.post("/learners", json={"prior_ability_score": 0.5})
    assert response.status_code == 200
    learner = response.json()
    assert learner["study_protocol_version"] == "v0.3"
    assert learner["learning_module_version"] == "v0.4.0"
    assert learner["system_prompt_version"] in (None, SYSTEM_PROMPT_VERSION)
    assert learner["ai_provider"] in (None, "groq")
    assert learner["ai_model"] in (None, "frozen-model")
    assert learner["ai_interaction_cap"] in (None, 8)
    assert learner["supported_phase_minutes"] == 20
    assert learner["participation_status"] == "active"


def test_no_ai_learner_freezes_non_ai_provenance_without_ai_config(
    client, monkeypatch
):
    monkeypatch.setattr("app.routers.learners.random.choice", lambda values: (
        "no_ai" if "no_ai" in values else "immediate_only"
    ))
    monkeypatch.setattr(settings, "llm_provider", "unsupported")
    monkeypatch.setattr(settings, "llm_model", None)
    response = client.post("/learners", json={})
    assert response.status_code == 200
    learner = response.json()
    assert learner["study_protocol_version"]
    assert learner["learning_module_version"]
    assert learner["supported_phase_minutes"] > 0
    assert learner["participation_status"] == "active"
    assert learner["system_prompt_version"] is None
    assert learner["ai_provider"] is None
    assert learner["ai_model"] is None
    assert learner["ai_interaction_cap"] is None


def test_runtime_changes_do_not_change_existing_learner(client, db_session, monkeypatch):
    monkeypatch.setattr(settings, "llm_model", "initial-model")
    response = client.post("/learners", json={})
    learner_id = response.json()["id"]
    expected = response.json()
    monkeypatch.setattr(settings, "llm_model", "new-model")
    fetched = client.get(f"/learners/{learner_id}").json()
    assert fetched["ai_model"] == expected["ai_model"]


def test_task_version_is_snapshotted(make_learner, make_task, make_attempt):
    learner = make_learner()
    task = make_task("immediate")
    attempt = make_attempt(learner, task)
    task.version = "changed"
    assert attempt.task_version == "0.3.1"


def test_frozen_duration_drives_expiry(client, db_session, make_learner, make_task, make_attempt):
    learner = make_learner()
    learner.supported_phase_minutes = 1
    task = make_task("supported")
    attempt = make_attempt(learner, task, started_at=datetime.utcnow() - timedelta(minutes=2))
    response = client.get(f"/tasks/learner/{learner.id}")
    assert response.status_code == 200
    db_session.refresh(attempt)
    assert attempt.supported_end_reason == "expired"


def test_frozen_cap_is_used_for_ai(client, make_learner, make_task, make_attempt, monkeypatch):
    configure_llm(monkeypatch)
    learner = make_learner()
    learner.ai_interaction_cap = 0
    task = make_task("supported")
    attempt = make_attempt(learner, task, started_at=datetime.utcnow())
    response = client.post("/ai/chat", json={"attempt_id": attempt.id, "message": "help"})
    assert response.status_code == 429


def test_frozen_model_is_sent_to_provider(client, make_learner, make_task, make_attempt, monkeypatch):
    configure_llm(monkeypatch)
    monkeypatch.setattr(settings, "llm_model", "frozen-model")
    learner = make_learner()
    learner.ai_model = "frozen-model"
    task = make_task("supported")
    attempt = make_attempt(learner, task, started_at=datetime.utcnow())
    with patch("app.routers.ai.httpx.post", return_value=fake_response()) as request:
        response = client.post("/ai/chat", json={"attempt_id": attempt.id, "message": "help"})
    assert response.status_code == 200
    assert request.call_args.kwargs["json"]["model"] == "frozen-model"


def test_provider_rejection_of_frozen_model_is_surfaced(
    client, make_learner, make_task, make_attempt, monkeypatch
):
    configure_llm(monkeypatch)
    learner = make_learner()
    learner.ai_model = "unknown-model"
    task = make_task("supported")
    attempt = make_attempt(learner, task, started_at=datetime.utcnow())
    with patch("app.routers.ai.httpx.post", side_effect=RuntimeError("model rejected")):
        response = client.post(
            "/ai/chat", json={"attempt_id": attempt.id, "message": "help"}
        )
    assert response.status_code == 502


def test_unknown_provider_fails_closed(client, make_learner, make_task, make_attempt, monkeypatch):
    configure_llm(monkeypatch)
    learner = make_learner()
    learner.ai_provider = "unknown-provider"
    task = make_task("supported")
    attempt = make_attempt(learner, task, started_at=datetime.utcnow())
    response = client.post("/ai/chat", json={"attempt_id": attempt.id, "message": "help"})
    assert response.status_code == 503


def test_unknown_prompt_version_fails_closed(client, make_learner, make_task, make_attempt, monkeypatch):
    configure_llm(monkeypatch)
    learner = make_learner()
    learner.system_prompt_version = "unknown"
    task = make_task("supported")
    attempt = make_attempt(learner, task, started_at=datetime.utcnow())
    response = client.post("/ai/chat", json={"attempt_id": attempt.id, "message": "help"})
    assert response.status_code == 503


def test_unknown_module_version_fails_closed(client, make_learner):
    learner = make_learner()
    learner.learning_module_version = "unknown"
    response = client.get(f"/learning/loops?learner_id={learner.id}")
    assert response.status_code == 503


def test_module_registry_keeps_frozen_version(monkeypatch, make_learner, client):
    learner = make_learner()
    original_released = MODULE_REGISTRY["v0.2.0"]
    original_current = MODULE_REGISTRY["v0.3.0"]
    MODULE_REGISTRY["vA"] = {"module_id": "loops", "version": "vA"}
    MODULE_REGISTRY["vB"] = {"module_id": "loops", "version": "vB"}
    learner.learning_module_version = "vA"
    monkeypatch.setattr(settings, "learning_module_version", "vB")
    response = client.get(f"/learning/loops?learner_id={learner.id}")
    assert response.json()["version"] == "vA"
    MODULE_REGISTRY["v0.2.0"] = original_released
    MODULE_REGISTRY["v0.3.0"] = original_current
    MODULE_REGISTRY.pop("vA")
    MODULE_REGISTRY.pop("vB")


def test_current_module_version_is_resolved_and_legacy_version_remains_available():
    assert "v0.4.0" in MODULE_REGISTRY
    assert "v0.3.0" in MODULE_REGISTRY
    assert "v0.2.0" in MODULE_REGISTRY
    assert MODULE_REGISTRY["v0.4.0"]["version"] == "v0.4.0"
    assert MODULE_REGISTRY["v0.3.0"]["version"] == "v0.3.0"
    assert MODULE_REGISTRY["v0.2.0"]["version"] == "v0.2.0"


def test_prompt_registry_keeps_frozen_version(monkeypatch, make_learner):
    learner = make_learner()
    learner.system_prompt_version = "vA"
    SYSTEM_PROMPT_REGISTRY["vA"] = "prompt A"
    SYSTEM_PROMPT_REGISTRY["vB"] = "prompt B"
    monkeypatch.setattr(settings, "system_prompt_version", "vB")
    from app.routers.ai import get_system_prompt
    assert get_system_prompt(learner.system_prompt_version) == "prompt A"
    SYSTEM_PROMPT_REGISTRY.pop("vA")
    SYSTEM_PROMPT_REGISTRY.pop("vB")


def test_unknown_registry_versions_fail_closed(client, make_learner, make_task, make_attempt, monkeypatch):
    learner = make_learner()
    task = make_task("supported")
    attempt = make_attempt(learner, task, started_at=datetime.utcnow())
    learner.system_prompt_version = "unknown"
    configure_llm(monkeypatch)
    assert client.post("/ai/chat", json={"attempt_id": attempt.id, "message": "help"}).status_code == 503
    learner.learning_module_version = "unknown"
    assert client.get(f"/learning/loops?learner_id={learner.id}").status_code == 503


def test_assessment_start_is_idempotent(client, db_session, make_learner, make_task, make_attempt):
    learner = make_learner()
    supported = make_task("supported")
    task = make_task("immediate")
    make_attempt(learner, supported, started_at=datetime.utcnow(), completed_at=datetime.utcnow())
    attempt = make_attempt(learner, task)
    first = client.post(f"/tasks/{task.id}/start?learner_id={learner.id}")
    original = first.json()["started_at"]
    second = client.post(f"/tasks/{task.id}/start?learner_id={learner.id}")
    assert first.status_code == second.status_code == 200
    assert second.json()["started_at"] == original
    db_session.refresh(attempt)
    assert attempt.started_at.isoformat() == original


def test_immediate_assessment_start_requires_supported_unlock(
    client, make_learner, make_task, make_attempt
):
    learner = make_learner()
    supported = make_task("supported")
    immediate = make_task("immediate")
    make_attempt(learner, supported, started_at=datetime.utcnow())
    make_attempt(learner, immediate)
    response = client.post(f"/tasks/{immediate.id}/start?learner_id={learner.id}")
    assert response.status_code == 409


def test_supported_completion_sets_end_reason(client, db_session, make_learner, make_task, make_attempt):
    learner = make_learner()
    task = make_task("supported")
    attempt = make_attempt(learner, task, started_at=datetime.utcnow())
    response = client.post(f"/tasks/{task.id}/submit?learner_id={learner.id}", json={"code": "def add(a,b):\n    return a+b"})
    assert response.status_code == 200
    db_session.refresh(attempt)
    assert attempt.supported_end_reason == "completed"
    assert attempt.grader_version == GRADER_VERSION


def test_grader_version_is_null_before_grading(db_session, make_learner, make_task, make_attempt):
    attempt = make_attempt(make_learner(), make_task("immediate"))
    assert attempt.grader_version is None


def test_all_independent_phases_can_start(
    client, make_learner, make_task, make_attempt
):
    learner = make_learner()
    supported = make_task("supported")
    supported_attempt = make_attempt(
        learner, supported, started_at=datetime.utcnow(), completed_at=datetime.utcnow()
    )
    for phase in ("immediate", "delayed", "transfer", "criterion"):
        task = make_task(phase)
        attempt = make_attempt(learner, task)
        response = client.post(f"/tasks/{task.id}/start?learner_id={learner.id}")
        assert response.status_code == 200
        assert response.json()["started_at"] == attempt.started_at.isoformat()


def test_generic_start_rejects_wrong_future_completed_and_supported(
    client, make_learner, make_task, make_attempt
):
    learner = make_learner()
    other = make_learner()
    supported = make_task("supported")
    immediate = make_task("immediate")
    future = make_task("delayed")
    completed = make_task("transfer")
    make_attempt(learner, supported, started_at=datetime.utcnow(), completed_at=datetime.utcnow())
    make_attempt(learner, immediate)
    make_attempt(learner, future, scheduled_for=datetime.utcnow() + timedelta(days=1))
    make_attempt(learner, completed, completed_at=datetime.utcnow())
    other_attempt = make_attempt(other, make_task("criterion"))
    assert client.post(f"/tasks/{other_attempt.task_id}/start?learner_id={learner.id}").status_code == 404
    assert client.post(f"/tasks/{future.id}/start?learner_id={learner.id}").status_code == 409
    assert client.post(f"/tasks/{completed.id}/start?learner_id={learner.id}").status_code == 409
    assert client.post(f"/tasks/{supported.id}/start?learner_id={learner.id}").status_code == 409


def test_expired_supported_start_is_rejected_and_immutable(
    client, db_session, make_learner, make_task, make_attempt
):
    learner = make_learner()
    task = make_task("supported")
    attempt = make_attempt(learner, task, started_at=datetime.utcnow() - timedelta(minutes=21))
    assert client.post(f"/learning/loops/start?learner_id={learner.id}").status_code == 409
    db_session.refresh(attempt)
    assert attempt.supported_end_reason == "expired"
    assert client.post(f"/learning/loops/start?learner_id={learner.id}").status_code == 409
    assert client.get(f"/learners/{learner.id}/status").status_code == 200
    assert client.post("/ai/chat", json={"attempt_id": attempt.id, "message": "help"}).status_code == 409
    assert client.post(f"/tasks/{task.id}/submit?learner_id={learner.id}", json={"code": "result = 0"}).status_code == 409
    db_session.refresh(attempt)
    assert attempt.supported_end_reason == "expired"


def test_completed_supported_end_reason_is_immutable(
    client, db_session, make_learner, make_task, make_attempt
):
    learner = make_learner()
    task = make_task("supported")
    attempt = make_attempt(learner, task, started_at=datetime.utcnow(), completed_at=datetime.utcnow())
    attempt.supported_end_reason = "completed"
    db_session.commit()
    assert client.get(f"/tasks/learner/{learner.id}").status_code == 200
    assert client.get(f"/learners/{learner.id}/status").status_code == 200
    assert client.post(f"/learning/loops/start?learner_id={learner.id}").status_code == 409
    db_session.refresh(attempt)
    assert attempt.supported_end_reason == "completed"


def test_withdrawal_blocks_all_activity_and_preserves_history(
    client, db_session, make_learner, make_task, make_attempt
):
    learner = make_learner()
    supported = make_task("supported")
    immediate = make_task("immediate")
    supported_attempt = make_attempt(learner, supported, started_at=datetime.utcnow())
    immediate_attempt = make_attempt(learner, immediate)
    interaction = AIInteraction(
        attempt_id=supported_attempt.id,
        prompt="help",
        response="answer",
        sequence_num=1,
    )
    db_session.add(interaction)
    db_session.commit()
    learner.participation_status = "withdrawn"
    db_session.commit()
    assert client.get(f"/learning/loops?learner_id={learner.id}").status_code == 403
    assert client.get(f"/tasks/learner/{learner.id}").status_code == 403
    assert client.post(f"/learning/loops/start?learner_id={learner.id}").status_code == 403
    assert client.post(f"/tasks/{immediate.id}/start?learner_id={learner.id}").status_code == 403
    assert client.post(f"/tasks/{immediate.id}/submit?learner_id={learner.id}", json={"code": "result = 0"}).status_code == 403
    assert client.post("/ai/chat", json={"attempt_id": supported_attempt.id, "message": "help"}).status_code == 403
    db_session.refresh(supported_attempt)
    db_session.refresh(immediate_attempt)
    assert supported_attempt.started_at is not None
    assert supported_attempt.completed_at is None
    assert supported_attempt.submitted_code is None
    assert db_session.query(AIInteraction).filter_by(id=interaction.id).count() == 1


def test_withdrawn_learner_is_blocked(client, make_learner, make_task, make_attempt):
    learner = make_learner()
    learner.participation_status = "withdrawn"
    task = make_task("immediate")
    make_attempt(learner, task)
    assert client.get(f"/tasks/learner/{learner.id}").status_code == 403
    assert client.get(f"/learning/loops?learner_id={learner.id}").status_code == 403
