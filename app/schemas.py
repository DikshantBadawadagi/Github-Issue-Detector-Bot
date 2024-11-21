from pydantic import BaseModel

class AnalyzePRRequest(BaseModel):
    repo_url: str
    pr_number: int
    github_token: str

class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    message: str = None
