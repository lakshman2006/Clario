users = [
    {"id": 1, "name": "Alice", "role": "learner"},
    {"id": 2, "name": "Bob", "role": "admin"},
]

resources = [
    {"id": 1, "title": "Python Basics", "type": "video"},
    {"id": 2, "title": "FastAPI Tutorial", "type": "article"},
]

schedules = [
    {"user_id": 1, "resource_ids": [1, 2], "day": "Monday"},
]
