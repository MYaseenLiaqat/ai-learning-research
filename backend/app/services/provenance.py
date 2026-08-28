class FrozenProvenanceError(Exception):
    """Raised when participant behavior lacks frozen research provenance."""


def require_common_provenance(learner):
    required = {
        "study_protocol_version": learner.study_protocol_version,
        "learning_module_version": learner.learning_module_version,
        "supported_phase_minutes": learner.supported_phase_minutes,
        "participation_status": learner.participation_status,
    }
    missing = [
        name for name, value in required.items()
        if value is None or (isinstance(value, str) and not value)
    ]
    if missing:
        raise FrozenProvenanceError(
            "Frozen learner provenance is incomplete: " + ", ".join(missing)
        )
    if learner.supported_phase_minutes <= 0:
        raise FrozenProvenanceError("Frozen Supported duration is invalid")
    if learner.participation_status not in {"active", "withdrawn"}:
        raise FrozenProvenanceError("Frozen participation status is invalid")


def require_ai_provenance(learner):
    require_common_provenance(learner)
    required = {
        "system_prompt_version": learner.system_prompt_version,
        "ai_provider": learner.ai_provider,
        "ai_model": learner.ai_model,
        "ai_interaction_cap": learner.ai_interaction_cap,
    }
    missing = [name for name, value in required.items() if value is None or value == ""]
    if missing:
        raise FrozenProvenanceError(
            "Frozen AI provenance is incomplete: " + ", ".join(missing)
        )
    if learner.ai_interaction_cap < 0:
        raise FrozenProvenanceError("Frozen AI interaction cap is invalid")
