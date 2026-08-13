from app.db import SessionLocal, init_db
from app.models import Concept, Task

TASK_VERSION = "0.1.0"

init_db()
db = SessionLocal()

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
                "A weather station recorded these temperatures:\n"
                "temperatures = [28, 32, 35, 29, 31, 27]\n"
                "Write a Python program that counts how many temperatures are "
                "strictly greater than 30.\n"
                "Assign your answer to a variable named `result`.\n"
                "Expected result: 3"
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
                "Given:\n"
                "scores = [42, 67, 81, 39, 55, 48, 72]\n"
                "Write a Python program that counts how many scores are greater "
                "than or equal to 50.\n"
                "Assign your answer to a variable named `result`.\n"
                "Expected result: 4"
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
                "Given:\n"
                "prices = [450, 1200, 850, 1700, 999, 1500]\n"
                "Write a Python program that returns the total price of products "
                "costing strictly more than 1000.\n"
                "Assign your answer to a variable named `result`.\n"
                "Expected result: 4400"
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
                "Given:\n"
                "temperatures = [25, 34, 29, 41, 31]\n"
                "Write a Python program that creates a new list containing only "
                "the temperatures strictly greater than 30, preserving the "
                "original order.\n"
                "Assign your answer to a variable named `result`.\n"
                "Expected result: [34, 41, 31]"
            ),
            grading_spec={
                "mode": "exec_result",
                "result_var": "result",
                "tests": [
                    {"inputs": {"temperatures": [25, 34, 29, 41, 31]}, "expected": [34, 41, 31]},
                    {"inputs": {"temperatures": []}, "expected": []},
                    {"inputs": {"temperatures": [30, 30]}, "expected": []},
                    {"inputs": {"temperatures": [31, 31]}, "expected": [31, 31]},
                    {"inputs": {"temperatures": [40, 20, 50]}, "expected": [40, 50]},
                    {"inputs": {"temperatures": [10, 20]}, "expected": []},
                ],
            },
            scheduled_offset_days=14,
        ),
        Task(
            concept_id=concepts["Loops"].id,
            type="criterion",
            version=TASK_VERSION,
            prompt_text=(
                "A payment system records transaction amounts.\n"
                "transactions = [250, 1750, 999, 2400, 1000, 1250]\n"
                "Write a Python program that returns the total value of "
                "transactions strictly greater than 1000. If no transaction "
                "qualifies, return 0.\n"
                "Assign your answer to a variable named `result`.\n"
                "Expected result: 5400"
            ),
            grading_spec={
                "mode": "exec_result",
                "result_var": "result",
                "tests": [
                    {"inputs": {"transactions": [250, 1750, 999, 2400, 1000, 1250]}, "expected": 5400},
                    {"inputs": {"transactions": []}, "expected": 0},
                    {"inputs": {"transactions": [500, 600]}, "expected": 0},
                    {"inputs": {"transactions": [1001]}, "expected": 1001},
                    {"inputs": {"transactions": [1500, 1500]}, "expected": 3000},
                    {"inputs": {"transactions": [1000, 1001]}, "expected": 1001},
                ],
            },
            scheduled_offset_days=21,
        ),
    ])
    db.commit()

db.close()
print("Seed complete.")