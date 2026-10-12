from typing import Optional
from sqlalchemy.orm import Session
from app import models, schemas
from app.security import hash_password

def create_organization(db: Session, item: schemas.OrganizationCreate):
    obj = models.Organization(name=item.name, type=item.type, country_code=item.country_code)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def list_organizations(db: Session):
    return db.query(models.Organization).all()

def get_organization(db: Session, organization_id: str):
    return db.query(models.Organization).filter(models.Organization.id == organization_id).first()

def create_role(db: Session, item: schemas.RoleCreate):
    obj = models.Role(name=item.name, description=item.description)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def list_roles(db: Session):
    return db.query(models.Role).all()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_id(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, item: schemas.UserRegister):
    obj = models.User(
        organization_id=item.organization_id,
        email=str(item.email),
        password_hash=hash_password(item.password),
        full_name=item.full_name,
        role_name=item.role_name,
        is_active=True,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def list_users(db: Session):
    return db.query(models.User).all()

def create_project(db: Session, item: schemas.ProjectCreate):
    obj = models.Project(
        organization_id=item.organization_id,
        name=item.name,
        sponsor_name=item.sponsor_name,
        study_type=item.study_type,
        status=item.status,
        created_by=item.created_by,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def list_projects(db: Session):
    return db.query(models.Project).all()

def get_project(db: Session, project_id: str):
    return db.query(models.Project).filter(models.Project.id == project_id).first()

def create_study_basic(db: Session, item: schemas.StudyBasicCreate):
    obj = models.StudyBasic(
        project_id=item.project_id,
        indication=item.indication,
        phase=item.phase,
        population_description=item.population_description,
        intervention_name=item.intervention_name,
        comparator_name=item.comparator_name,
        blinding_method=item.blinding_method,
        randomization_method=item.randomization_method,
        study_duration_weeks=item.study_duration_weeks,
        target_sample_size=item.target_sample_size,
        expected_dropout_rate=item.expected_dropout_rate,
        primary_objective=item.primary_objective,
        secondary_objectives=item.secondary_objectives,
        primary_endpoint=item.primary_endpoint,
        secondary_endpoints=item.secondary_endpoints,
        safety_focus=item.safety_focus,
        study_aims=item.study_aims,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_study_basic_by_project(db: Session, project_id: str):
    return db.query(models.StudyBasic).filter(models.StudyBasic.project_id == project_id).first()

def create_study_design(db: Session, item: schemas.StudyDesignCreate):
    obj = models.StudyDesign(
        project_id=item.project_id,
        design_type=item.design_type,
        allocation_ratio=item.allocation_ratio,
        treatment_duration_weeks=item.treatment_duration_weeks,
        follow_up_weeks=item.follow_up_weeks,
        inclusion_summary=item.inclusion_summary,
        exclusion_summary=item.exclusion_summary,
        number_of_arms=item.number_of_arms,
        is_therapeutic=item.is_therapeutic,
        is_interventional=item.is_interventional,
        is_randomized=item.is_randomized,
        is_blinded=item.is_blinded,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_study_design_by_project(db: Session, project_id: str):
    return db.query(models.StudyDesign).filter(models.StudyDesign.project_id == project_id).first()

def create_protocol_version(db: Session, item: schemas.ProtocolVersionCreate):
    obj = models.ProtocolVersion(
        project_id=item.project_id,
        version_number=item.version_number,
        title=item.title,
        status=item.status,
        created_by=item.created_by,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def list_protocol_versions(db: Session, project_id: str):
    return db.query(models.ProtocolVersion).filter(models.ProtocolVersion.project_id == project_id).all()

def get_protocol_version(db: Session, version_id: str):
    return db.query(models.ProtocolVersion).filter(models.ProtocolVersion.id == version_id).first()

def create_protocol_section(db: Session, item: schemas.ProtocolSectionCreate):
    obj = models.ProtocolSection(
        version_id=item.version_id,
        section_code=item.section_code,
        section_title=item.section_title,
        content=item.content,
        is_generated=item.is_generated,
        generation_model=item.generation_model,
        source_reference=item.source_reference,
        revision_count=item.revision_count,
        last_modified_by=item.last_modified_by,
        confidence_score=item.confidence_score,
        needs_human_review=item.needs_human_review,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def list_protocol_sections(db: Session, version_id: str):
    return db.query(models.ProtocolSection).filter(models.ProtocolSection.version_id == version_id).all()

def create_review_comment(db: Session, item: schemas.ReviewCommentCreate):
    obj = models.ReviewComment(
        version_id=item.version_id,
        section_id=item.section_id,
        reviewer_user_id=item.reviewer_user_id,
        comment=item.comment,
        severity=item.severity,
        status=item.status,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def list_review_comments(db: Session, version_id: str):
    return db.query(models.ReviewComment).filter(models.ReviewComment.version_id == version_id).all()

def create_validation_result(db: Session, item: schemas.ValidationResultCreate):
    obj = models.ValidationResult(
        version_id=item.version_id,
        rule_code=item.rule_code,
        rule_name=item.rule_name,
        severity=item.severity,
        passed=item.passed,
        message=item.message,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def list_validation_results(db: Session, version_id: str):
    return db.query(models.ValidationResult).filter(models.ValidationResult.version_id == version_id).all()

def create_source_document(db: Session, item: schemas.SourceDocumentCreate):
    obj = models.SourceDocument(
        project_id=item.project_id,
        title=item.title,
        category=item.category,
        storage_path=item.storage_path,
        file_hash=item.file_hash,
        source_type=item.source_type,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def list_source_documents(db: Session, project_id: Optional[str] = None):
    if project_id:
        return db.query(models.SourceDocument).filter(models.SourceDocument.project_id == project_id).all()
    return db.query(models.SourceDocument).all()

def create_guideline_document(db: Session, item: schemas.GuidelineDocumentCreate):
    obj = models.GuidelineDocument(
        title=item.title,
        category=item.category,
        version=item.version,
        source_url=item.source_url,
        content=item.content,
        metadata=item.metadata,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def list_guideline_documents(db: Session):
    return db.query(models.GuidelineDocument).all()

def create_task(db: Session, item: schemas.TaskCreate):
    obj = models.TaskRecord(
        project_id=item.project_id,
        version_id=item.version_id,
        task_name=item.task_name,
        status=item.status,
        payload=item.payload,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def list_tasks(db: Session):
    return db.query(models.TaskRecord).all()

def get_task(db: Session, task_id: str):
    return db.query(models.TaskRecord).filter(models.TaskRecord.id == task_id).first()

def update_task_status(db: Session, task_id: str, status: str, result: Optional[dict] = None, error_message: Optional[str] = None):
    task = get_task(db, task_id)
    if not task:
        return None
    task.status = status
    task.result = result
    task.error_message = error_message
    db.commit()
    db.refresh(task)
    return task

def create_audit_log(db: Session, user_id: Optional[str], project_id: Optional[str], version_id: Optional[str], action_type: str, entity_type: Optional[str], entity_id: Optional[str], details: Optional[dict]):
    obj = models.AuditLog(
        user_id=user_id,
        project_id=project_id,
        version_id=version_id,
        action_type=action_type,
        entity_type=entity_type,
        entity_id=entity_id,
        details=details,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def list_audit_logs(db: Session):
    return db.query(models.AuditLog).all()
