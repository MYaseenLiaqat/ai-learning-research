import requests

BASE = "http://127.0.0.1:8000"

learner = requests.post(
    BASE + "/learners",
    json={"prior_ability_score": 0.5},
).json()

print("Learner:", learner)
print("Tasks:", requests.get(f"{BASE}/tasks/learner/{learner['id']}").json())
print("Health:", requests.get(BASE + "/health").json())
