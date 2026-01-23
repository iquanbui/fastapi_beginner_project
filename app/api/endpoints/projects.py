from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.project import Project, ProjectCreate

router = APIRouter()

# Mock database
fake_project_db = [
    {"id": 1, "name": "First Project", "description": "This is the first project"},
    {"id": 2, "name": "Second Project", "description": "This is the second project"},
]


@router.get("/", response_model=List[Project])
def read_projects(skip: int = 0, limit: int = 10):
    return fake_project_db[skip: skip + limit]


@router.get("/{project_id}", response_model=Project)
def read_project(project_id: int):
    for project in fake_project_db:
        if project["id"] == project_id:
            return project
    raise HTTPException(status_code=404, detail="Project not found")


@router.post("/", response_model=Project)
def create_project(project: ProjectCreate):
    new_project_id = len(fake_project_db) + 1
    new_project = project.dict()
    new_project["id"] = new_project_id
    fake_project_db.append(new_project)
    return new_project
