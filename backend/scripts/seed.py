from app.models import Concept, Task

TASK_VERSION = "0.5.0"


def seed(db):
    if db.query(Concept).count() == 0:
        db.add_all([
            Concept(name="Loops", order=1),
        ])
        db.commit()

    concepts = {c.name: c for c in db.query(Concept).all()}

    if db.query(Task).count() == 0:
        # Loops pilot tasks per research/loops_task_instrument_v0.5.0.md
        # All tasks use the provided-input + `result` variable contract.
        db.add_all([
        Task(
            concept_id=concepts["Loops"].id,
            type="supported",
            version=TASK_VERSION,
            prompt_text=(
                "The platform already provides a variable named `temperatures` containing:\n"
                "[28, 32, 35, 29, 31, 27]\n\n"
                "Do not redefine `temperatures`.\n\n"
                "Write Python code that sets `result` to the number of temperatures "
                "strictly greater than 30."
            ),
            grading_spec={
                "mode": "exec_result",
                "result_var": "result",
                "tests": [
                    {"inputs": {"temperatures": [28, 32, 35, 29, 31, 27]}, "expected": 3},
                    {"inputs": {"temperatures": []}, "expected": 0},
                    {"inputs": {"temperatures": [30, 30]}, "expected": 0},
                    {"inputs": {"temperatures": [31, 31]}, "expected": 2},
                    {"inputs": {"temperatures": [10, 20, 29]}, "expected": 0},
                    {"inputs": {"temperatures": [40, 50]}, "expected": 2},
                ],
            },
            scheduled_offset_days=0,
        ),
        Task(
            concept_id=concepts["Loops"].id,
            type="immediate",
            version=TASK_VERSION,
            prompt_text=(
                "The platform already provides a variable named `scores` containing:\n"
                "[42, 67, 81, 39, 55, 48, 72]\n\n"
                "Do not redefine `scores`.\n\n"
                "Write Python code that sets `result` to the number of scores that are "
                "greater than or equal to 50."
            ),
            grading_spec={
                "mode": "exec_result",
                "result_var": "result",
                "tests": [
                    {"inputs": {"scores": [42, 67, 81, 39, 55, 48, 72]}, "expected": 4},
                    {"inputs": {"scores": []}, "expected": 0},
                    {"inputs": {"scores": [49, 50, 51]}, "expected": 2},
                    {"inputs": {"scores": [50, 50]}, "expected": 2},
                    {"inputs": {"scores": [10, 20, 49]}, "expected": 0},
                    {"inputs": {"scores": [60, 70]}, "expected": 2},
                ],
            },
            scheduled_offset_days=0,
        ),
        Task(
            concept_id=concepts["Loops"].id,
            type="delayed",
            version=TASK_VERSION,
            prompt_text=(
                "The platform already provides a variable named `ages` containing:\n"
                "[12, 18, 7, 21, 16, 30]\n\n"
                "Do not redefine `ages`.\n\n"
                "Write Python code that sets `result` to the number of ages "
                "strictly less than 18."
            ),
            grading_spec={
                "mode": "exec_result",
                "result_var": "result",
                "tests": [
                    {"inputs": {"ages": [12, 18, 7, 21, 16, 30]}, "expected": 3},
                    {"inputs": {"ages": []}, "expected": 0},
                    {"inputs": {"ages": [18]}, "expected": 0},
                    {"inputs": {"ages": [17]}, "expected": 1},
                    {"inputs": {"ages": [5, 10, 15]}, "expected": 3},
                    {"inputs": {"ages": [20, 30]}, "expected": 0},
                ],
            },
            scheduled_offset_days=7,
        ),
        Task(
            concept_id=concepts["Loops"].id,
            type="transfer",
            version=TASK_VERSION,
            prompt_text=(
                "The platform already provides a variable named `scores` containing:\n"
                "[72, 91, 64, 88, 79]\n\n"
                "Do not redefine `scores`.\n\n"
                "Write Python code that sets `result` to the largest score. "
                "If the list is empty, set `result` to 0."
            ),
            grading_spec={
                "mode": "exec_result",
                "result_var": "result",
                "tests": [
                    {"inputs": {"scores": [72, 91, 64, 88, 79]}, "expected": 91},
                    {"inputs": {"scores": []}, "expected": 0},
                    {"inputs": {"scores": [42]}, "expected": 42},
                    {"inputs": {"scores": [75, 75]}, "expected": 75},
                    {"inputs": {"scores": [10, 99, 30]}, "expected": 99},
                    {"inputs": {"scores": [0, 1]}, "expected": 1},
                ],
            },
            scheduled_offset_days=14,
        ),
        Task(
            concept_id=concepts["Loops"].id,
            type="criterion",
            version=TASK_VERSION,
            prompt_text=(
                "The platform already provides a variable named `activity` containing:\n"
                "[\"yes\", \"yes\", \"no\", \"yes\", \"yes\", \"yes\", \"no\"]\n\n"
                "Do not redefine `activity`.\n\n"
                "Write Python code that sets `result` to the length of the longest consecutive "
                "streak of \"yes\" values. Use a current-streak state and a best-streak state."
            ),
            grading_spec={
                "mode": "exec_result",
                "result_var": "result",
                "tests": [
                    {"inputs": {"activity": ["yes", "yes", "no", "yes", "yes", "yes", "no"]}, "expected": 3},
                    {"inputs": {"activity": []}, "expected": 0},
                    {"inputs": {"activity": ["no", "no"]}, "expected": 0},
                    {"inputs": {"activity": ["yes"]}, "expected": 1},
                    {"inputs": {"activity": ["yes", "yes"]}, "expected": 2},
                    {"inputs": {"activity": ["yes", "no", "yes", "yes"]}, "expected": 2},
                ],
            },
            scheduled_offset_days=21,
        ),
        ])
        db.commit()


if __name__ == "__main__":
    from app.db import SessionLocal, init_db

    init_db()
    with SessionLocal() as db:
        seed(db)
    print("Seed complete.")
