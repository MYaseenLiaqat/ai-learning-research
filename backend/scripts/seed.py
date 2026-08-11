from app.db import SessionLocal, init_db
from app.models import Concept, Task

init_db()
db = SessionLocal()

if db.query(Concept).count() == 0:
    db.add_all([
        Concept(name="Functions", order=1),
        Concept(name="Lists", order=2),
        Concept(name="Conditionals", order=3),
    ])
    db.commit()

concepts = {c.name: c for c in db.query(Concept).all()}

if db.query(Task).count() == 0:
    db.add_all([
        Task(
            concept_id=concepts["Functions"].id,
            type="supported",
            prompt_text="Write average(values) returning the arithmetic mean.",
            grading_spec={"tests": [
                {"expression": "average([1,2,3])", "expected": 2.0},
                {"expression": "average([10,20])", "expected": 15.0},
            ]},
            scheduled_offset_days=0,
        ),
        Task(
            concept_id=concepts["Functions"].id,
            type="immediate",
            prompt_text="Write double_sum(values) returning twice the sum.",
            grading_spec={"tests": [
                {"expression": "double_sum([1,2,3])", "expected": 12},
                {"expression": "double_sum([5])", "expected": 10},
                {"expression": "double_sum([])", "expected": 0},
            ]},
            scheduled_offset_days=0,
        ),
        Task(
            concept_id=concepts["Lists"].id,
            type="delayed",
            prompt_text="Write positive_values(values) returning only positive numbers.",
            grading_spec={"tests": [
                {"expression": "positive_values([-2,0,3,5])", "expected": [3,5]},
                {"expression": "positive_values([-1,-4])", "expected": []},
            ]},
            scheduled_offset_days=7,
        ),
        Task(
            concept_id=concepts["Conditionals"].id,
            type="transfer",
            prompt_text="Write classify_score(score): high >=80, medium >=50, otherwise low.",
            grading_spec={"tests": [
                {"expression": "classify_score(90)", "expected": "high"},
                {"expression": "classify_score(70)", "expected": "medium"},
                {"expression": "classify_score(40)", "expected": "low"},
            ]},
            scheduled_offset_days=14,
        ),
        Task(
            concept_id=concepts["Lists"].id,
            type="criterion",
            prompt_text="Write sum_positive(values) returning the sum of positive values.",
            grading_spec={"tests": [
                {"expression": "sum_positive([-2,3,5,-1])", "expected": 8},
                {"expression": "sum_positive([-3,-4])", "expected": 0},
            ]},
            scheduled_offset_days=21,
        ),
    ])
    db.commit()

db.close()
print("Seed complete.")
