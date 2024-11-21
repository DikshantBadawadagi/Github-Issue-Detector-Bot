from fastapi import FastAPI, HTTPException
from app.schemas import AnalyzePRRequest, TaskStatusResponse
from app.db import create_task, get_task, update_task
from app.tasks import analyze_pull_request

app = FastAPI()

from app.celery_app import celery_app
from celery.result import AsyncResult

@celery_app.task(bind=True)

def analyze_pull_request(self, repo_url, pr_number, github_token):
    print(f"Task received with repo_url={repo_url}, pr_number={pr_number}")
    return {"status": "success"}

# FastAPI endpoint example
@app.post("/analyze-pr")
async def analyze_pr(request: AnalyzePRRequest):
    try:
        # Schedule the task
        task = analyze_pull_request.apply_async(
            args=[request.repo_url, request.pr_number, request.github_token]
        )
        
        return {
            "task_id": task.id,  # Important: capture the task ID
            "status": "pending"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# Simulate a task call
# result = analyze_pull_request("https://github.com/user/repo", 123, "test_token")
# print(result)

# @app.post("/analyze-pr", response_model=TaskStatusResponse)
# def analyze_pr(request: AnalyzePRRequest):
#     # Create a task ID
#     task_id = create_task()

#     # Schedule the task asynchronously
#     result = analyze_pull_request.apply_async(
#         args=[request.repo_url, request.pr_number, request.github_token],
#         task_id=task_id
#     )
#     print(result)
#     return TaskStatusResponse(task_id=task_id, status="processing")

@app.get("/status/{task_id}", response_model=TaskStatusResponse)
def get_status(task_id: str):
    task = get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskStatusResponse(task_id=task_id, status=task["status"])

@app.get("/results/{task_id}", response_model=TaskStatusResponse)
def get_results(task_id: str):
    task = get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if not task["results"]:
        raise HTTPException(status_code=202, detail="Results not ready")
    return TaskStatusResponse(task_id=task_id, status="completed", message=task["results"])
