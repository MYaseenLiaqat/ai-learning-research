from app.models import Concept, Task

TASK_VERSION = "0.3.1"


def seed(db):
    if db.query(Concept).count() == 0:
        db.add_all([
            Concept(name="Loops", order=1),
        ])
        db.commit()

    concepts = {c.name: c for c in db.query(Concept).all()}

    if db.query(Task).count() == 0:
        # Loops pilot tasks per research/loops_learning_module_v0.2.md
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
                "The platform already provides a variable named `prices` containing:\n"
                "[450, 1200, 850, 1700, 999, 1500]\n\n"
                "Do not redefine `prices`.\n\n"
                "Write Python code that sets `result` to the total price of products "
                "strictly more than 1000."
            ),
            grading_spec={
                "mode": "exec_result",
                "result_var": "result",
                "tests": [
                    {"inputs": {"prices": [450, 1200, 850, 1700, 999, 1500]}, "expected": 4400},
                    {"inputs": {"prices": []}, "expected": 0},
                    {"inputs": {"prices": [1000]}, "expected": 0},
                    {"inputs": {"prices": [1001]}, "expected": 1001},
                    {"inputs": {"prices": [1200, 1200]}, "expected": 2400},
                    {"inputs": {"prices": [500, 600]}, "expected": 0},
                ],
            },
            scheduled_offset_days=7,
        ),
        Task(
            concept_id=concepts["Loops"].id,
            type="transfer",
            version=TASK_VERSION,
            prompt_text=(
                "The platform already provides a variable named `readings` containing:\n"
                "[18, 42, 29, 51, 33]\n\n"
                "Do not redefine `readings`.\n\n"
                "Write Python code that sets `result` to the total amount by which readings "
                "above 30 exceed 30. For example, a reading of 42 contributes 12 because "
                "42 - 30 = 12."
            ),
            grading_spec={
                "mode": "exec_result",
                "result_var": "result",
                "tests": [
                    {"inputs": {"readings": [18, 42, 29, 51, 33]}, "expected": 36},
                    {"inputs": {"readings": []}, "expected": 0},
                    {"inputs": {"readings": [30, 30]}, "expected": 0},
                    {"inputs": {"readings": [31, 31]}, "expected": 2},
                    {"inputs": {"readings": [40, 20, 50]}, "expected": 30},
                    {"inputs": {"readings": [10, 20]}, "expected": 0},
                ],
            },
            scheduled_offset_days=14,
        ),
        Task(
            concept_id=concepts["Loops"].id,
            type="criterion",
            version=TASK_VERSION,
            prompt_text=(
                "The platform already provides a variable named `hours` containing:\n"
                "[5, 12, 8, 17, 9, 14]\n\n"
                "Do not redefine `hours`.\n\n"
                "A long shift is a shift that lasts at least 10 hours. Write Python code that sets `result` "
                "to the total hours worked across all long shifts. If no shift qualifies, set `result` to 0."
            ),
            grading_spec={
                "mode": "exec_result",
                "result_var": "result",
                "tests": [
                    {"inputs": {"hours": [5, 12, 8, 17, 9, 14]}, "expected": 43},
                    {"inputs": {"hours": []}, "expected": 0},
                    {"inputs": {"hours": [9, 8, 7]}, "expected": 0},
                    {"inputs": {"hours": [10]}, "expected": 10},
                    {"inputs": {"hours": [10, 10]}, "expected": 20},
                    {"inputs": {"hours": [9, 10, 12]}, "expected": 22},
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
