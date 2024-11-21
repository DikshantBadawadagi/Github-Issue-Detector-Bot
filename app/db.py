import uuid

# Simulated database for tasks
TASK_DB = {}

def create_task():
    task_id = str(uuid.uuid4())
    TASK_DB[task_id] = {"status": "pending", "results": None}
    return task_id

def update_task(task_id, status, results=None):
    if task_id in TASK_DB:
        TASK_DB[task_id] = {"status": status, "results": results}

def get_task(task_id):
    return TASK_DB.get(task_id, None)
