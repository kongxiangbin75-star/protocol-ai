import os
from datetime import timedelta
from typing import Optional

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.config import settings
from app.database import Base, engine, get_db
from app.security import create_access_token, get_current_active_user, verify_password

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name, version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def root():
    return {"message": "Protocol AI backend is running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/auth/register", response_model=schemas.UserRead)
def register_user(item: schemas.UserRegister, db: Session = Depends(get_db)):
    if crud.get_user_by_email(db, str(item.email)):
        raise HTTPException(status_code=400, detail="User already exists")
    user = crud.create_user(db, item)
    return user

@app.post("/auth/login", response_model=schemas.Token)
def login_user(item: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, str(item.email))
    if not user or not verify_password(item.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(user.email, timedelta(minutes=settings.access_token_expire_minutes))
    return {"access_token": token, "token_type": "bearer"}

@app.get("/auth/me", response_model=schemas.UserRead)
def get_me(current_user: models.User = Depends(get_current_active_user)):
    return current_user

@app.post("/organizations/", response_model=schemas.OrganizationRead)
def create_organization(item: schemas.OrganizationCreate, db: Session = Depends(get_db)):
    return crud.create_organization(db, item)

@app.get("/organizations/", response_model=list[schemas.OrganizationRead])
def list_organizations(db: Session = Depends(get_db)):
    return crud.list_organizations(db)

@app.post("/roles/", response_model=schemas.RoleRead)
def create_role(item: schemas.RoleCreate, db: Session = Depends(get_db)):
    return crud.create_role(db, item)

@app.get("/roles/", response_model=list[schemas.RoleRead])
def list_roles(db: Session = Depends(get_db)):
    return crud.list_roles(db)

@app.get("/users/", response_model=list[schemas.UserRead])
def list_users(db: Session = Depends(get_db)):
    return crud.list_users(db)

@app.post("/projects/", response_model=schemas.ProjectRead)
def create_project(item: schemas.ProjectCreate, db: Session = Depends(get_db)):
    return crud.create_project(db, item)

@app.get("/projects/", response_model=list[schemas.ProjectRead])
def list_projects(db: Session = Depends(get_db)):
    return crud.list_projects(db)

@app.get("/projects/{project_id}", response_model=schemas.ProjectRead)
def get_project(project_id: str, db: Session = Depends(get_db)):
    project = crud.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@app.post("/study-basics/", response_model=schemas.StudyBasicRead)
def create_study_basic(item: schemas.StudyBasicCreate, db: Session = Depends(get_db)):
    project = crud.get_project(db, item.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    existing = crud.get_study_basic_by_project(db, item.project_id)
    if existing:
        raise HTTPException(status_code=400, detail="StudyBasic already exists for this project")
    return crud.create_study_basic(db, item)

@app.get("/study-basics/{project_id}", response_model=schemas.StudyBasicRead)
def get_study_basic(project_id: str, db: Session = Depends(get_db)):
    item = crud.get_study_basic_by_project(db, project_id)
    if not item:
        raise HTTPException(status_code=404, detail="StudyBasic not found")
    return item

@app.post("/study-designs/", response_model=schemas.StudyDesignRead)
def create_study_design(item: schemas.StudyDesignCreate, db: Session = Depends(get_db)):
    project = crud.get_project(db, item.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    existing = crud.get_study_design_by_project(db, item.project_id)
    if existing:
        raise HTTPException(status_code=400, detail="StudyDesign already exists for this project")
    return crud.create_study_design(db, item)

@app.get("/study-designs/{project_id}", response_model=schemas.StudyDesignRead)
def get_study_design(project_id: str, db: Session = Depends(get_db)):
    item = crud.get_study_design_by_project(db, project_id)
    if not item:
        raise HTTPException(status_code=404, detail="StudyDesign not found")
    return item

@app.post("/protocol-versions/", response_model=schemas.ProtocolVersionRead)
def create_protocol_version(item: schemas.ProtocolVersionCreate, db: Session = Depends(get_db)):
    project = crud.get_project(db, item.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return crud.create_protocol_version(db, item)

@app.get("/protocol-versions/{project_id}", response_model=list[schemas.ProtocolVersionRead])
def list_protocol_versions(project_id: str, db: Session = Depends(get_db)):
    project = crud.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return crud.list_protocol_versions(db, project_id)

@app.post("/protocol-sections/", response_model=schemas.ProtocolSectionRead)
def create_protocol_section(item: schemas.ProtocolSectionCreate, db: Session = Depends(get_db)):
    version = crud.get_protocol_version(db, item.version_id)
    if not version:
        raise HTTPException(status_code=404, detail="Protocol version not found")
    return crud.create_protocol_section(db, item)

@app.get("/protocol-sections/{version_id}", response_model=list[schemas.ProtocolSectionRead])
def list_sections(version_id: str, db: Session = Depends(get_db)):
    version = crud.get_protocol_version(db, version_id)
    if not version:
        raise HTTPException(status_code=404, detail="Protocol version not found")
    return crud.list_protocol_sections(db, version_id)

@app.post("/review-comments/", response_model=schemas.ReviewCommentRead)
def create_review_comment(item: schemas.ReviewCommentCreate, db: Session = Depends(get_db)):
    version = crud.get_protocol_version(db, item.version_id)
    if not version:
        raise HTTPException(status_code=404, detail="Protocol version not found")
    return crud.create_review_comment(db, item)

@app.get("/review-comments/{version_id}", response_model=list[schemas.ReviewCommentRead])
def list_review_comments(version_id: str, db: Session = Depends(get_db)):
    version = crud.get_protocol_version(db, version_id)
    if not version:
        raise HTTPException(status_code=404, detail="Protocol version not found")
    return crud.list_review_comments(db, version_id)

@app.post("/validation-results/", response_model=schemas.ValidationResultRead)
def create_validation_result(item: schemas.ValidationResultCreate, db: Session = Depends(get_db)):
    version = crud.get_protocol_version(db, item.version_id)
    if not version:
        raise HTTPException(status_code=404, detail="Protocol version not found")
    return crud.create_validation_result(db, item)

@app.get("/validation-results/{version_id}", response_model=list[schemas.ValidationResultRead])
def list_validation_results(version_id: str, db: Session = Depends(get_db)):
    version = crud.get_protocol_version(db, version_id)
    if not version:
        raise HTTPException(status_code=404, detail="Protocol version not found")
    return crud.list_validation_results(db, version_id)

@app.post("/documents/upload")
async def upload_document(file: UploadFile = File(...), project_id: Optional[str] = None, db: Session = Depends(get_db)):
    file_name = file.filename or "upload.bin"
    file_path = os.path.join(UPLOAD_DIR, file_name)
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    item = schemas.SourceDocumentCreate(
        project_id=project_id,
        title=file_name,
        category="uploaded",
        storage_path=file_path,
        file_hash=None,
        source_type="uploaded",
    )
    doc = crud.create_source_document(db, item)
    return {"id": doc.id, "path": file_path}

@app.get("/documents")
def list_documents(project_id: Optional[str] = None, db: Session = Depends(get_db)):
    return crud.list_source_documents(db, project_id)

@app.post("/guidelines/", response_model=schemas.GuidelineDocumentRead)
def create_guideline(item: schemas.GuidelineDocumentCreate, db: Session = Depends(get_db)):
    return crud.create_guideline_document(db, item)

@app.get("/guidelines/", response_model=list[schemas.GuidelineDocumentRead])
def list_guidelines(db: Session = Depends(get_db)):
    return crud.list_guideline_documents(db)

@app.post("/tasks/", response_model=schemas.TaskRead)
def create_task(item: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db, item)

@app.get("/tasks/", response_model=list[schemas.TaskRead])
def list_tasks(db: Session = Depends(get_db)):
    return crud.list_tasks(db)

@app.get("/tasks/{task_id}", response_model=schemas.TaskRead)
def get_task(task_id: str, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.get("/audit-logs/", response_model=list[schemas.AuditLogRead])
def list_audit_logs(db: Session = Depends(get_db)):
    return crud.list_audit_logs(db)
