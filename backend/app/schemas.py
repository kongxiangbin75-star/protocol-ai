from typing import Optional, Any
from pydantic import BaseModel, ConfigDict, EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    organization_id: Optional[str] = None
    role_name: str = "member"

class OrganizationCreate(BaseModel):
    name: str
    type: str = "company"
    country_code: Optional[str] = None

class OrganizationRead(BaseModel):
    id: str
    name: str
    type: str
    country_code: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class RoleCreate(BaseModel):
    name: str
    description: Optional[str] = None

class RoleRead(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class UserRead(BaseModel):
    id: str
    organization_id: Optional[str]
    email: EmailStr
    full_name: str
    role_name: str
    is_active: bool
    model_config = ConfigDict(from_attributes=True)

class ProjectCreate(BaseModel):
    organization_id: Optional[str] = None
    name: str
    sponsor_name: Optional[str] = None
    study_type: str = "interventional"
    status: str = "draft"
    created_by: Optional[str] = None

class ProjectRead(BaseModel):
    id: str
    organization_id: Optional[str]
    name: str
    sponsor_name: Optional[str]
    study_type: str
    status: str
    created_by: Optional[str]
    model_config = ConfigDict(from_attributes=True)

class StudyBasicCreate(BaseModel):
    project_id: str
    indication: str
    phase: str
    population_description: Optional[str] = None
    intervention_name: Optional[str] = None
    comparator_name: Optional[str] = None
    blinding_method: Optional[str] = None
    randomization_method: Optional[str] = None
    study_duration_weeks: Optional[int] = None
    target_sample_size: Optional[int] = None
    expected_dropout_rate: Optional[float] = None
    primary_objective: Optional[str] = None
    secondary_objectives: Optional[str] = None
    primary_endpoint: Optional[str] = None
    secondary_endpoints: Optional[str] = None
    safety_focus: Optional[str] = None
    study_aims: Optional[str] = None

class StudyBasicRead(StudyBasicCreate):
    id: str
    model_config = ConfigDict(from_attributes=True)

class StudyDesignCreate(BaseModel):
    project_id: str
    design_type: str
    allocation_ratio: Optional[str] = None
    treatment_duration_weeks: Optional[int] = None
    follow_up_weeks: Optional[int] = None
    inclusion_summary: Optional[str] = None
    exclusion_summary: Optional[str] = None
    number_of_arms: Optional[int] = None
    is_therapeutic: bool = False
    is_interventional: bool = True
    is_randomized: bool = False
    is_blinded: bool = False

class StudyDesignRead(StudyDesignCreate):
    id: str
    model_config = ConfigDict(from_attributes=True)

class ProtocolVersionCreate(BaseModel):
    project_id: str
    version_number: str
    title: str
    status: str = "draft"
    created_by: Optional[str] = None

class ProtocolVersionRead(BaseModel):
    id: str
    project_id: str
    version_number: str
    title: str
    status: str
    created_by: Optional[str]
    approved_by: Optional[str]
    approved_at: Optional[str]
    model_config = ConfigDict(from_attributes=True)

class ProtocolSectionCreate(BaseModel):
    version_id: str
    section_code: str
    section_title: str
    content: Optional[str] = None
    is_generated: bool = True
    generation_model: Optional[str] = None
    source_reference: Optional[str] = None
    revision_count: int = 0
    last_modified_by: Optional[str] = None
    confidence_score: Optional[float] = None
    needs_human_review: bool = False

class ProtocolSectionRead(ProtocolSectionCreate):
    id: str
    model_config = ConfigDict(from_attributes=True)

class ReviewCommentCreate(BaseModel):
    version_id: str
    section_id: Optional[str] = None
    reviewer_user_id: str
    comment: str
    severity: str = "medium"
    status: str = "open"

class ReviewCommentRead(ReviewCommentCreate):
    id: str
    created_at: Optional[str]
    model_config = ConfigDict(from_attributes=True)

class ValidationResultCreate(BaseModel):
    version_id: str
    rule_code: str
    rule_name: str
    severity: str = "medium"
    passed: bool = False
    message: Optional[str] = None

class ValidationResultRead(ValidationResultCreate):
    id: str
    created_at: Optional[str]
    model_config = ConfigDict(from_attributes=True)

class SourceDocumentCreate(BaseModel):
    project_id: Optional[str] = None
    title: str
    category: Optional[str] = None
    storage_path: str
    file_hash: Optional[str] = None
    source_type: str = "uploaded"

class SourceDocumentRead(SourceDocumentCreate):
    id: str
    created_at: Optional[str]
    model_config = ConfigDict(from_attributes=True)

class GuidelineDocumentCreate(BaseModel):
    title: str
    category: str
    version: Optional[str] = None
    source_url: Optional[str] = None
    content: Optional[str] = None
    metadata: Optional[Any] = None

class GuidelineDocumentRead(GuidelineDocumentCreate):
    id: str
    created_at: Optional[str]
    model_config = ConfigDict(from_attributes=True)

class TaskCreate(BaseModel):
    project_id: Optional[str] = None
    version_id: Optional[str] = None
    task_name: str
    status: str = "queued"
    payload: Optional[Any] = None

class TaskRead(TaskCreate):
    id: str
    result: Optional[Any] = None
    error_message: Optional[str] = None
    created_at: Optional[str]
    updated_at: Optional[str]
    model_config = ConfigDict(from_attributes=True)

class AuditLogRead(BaseModel):
    id: str
    project_id: Optional[str]
    version_id: Optional[str]
    user_id: Optional[str]
    action_type: str
    entity_type: Optional[str]
    entity_id: Optional[str]
    details: Optional[Any]
    created_at: Optional[str]
    model_config = ConfigDict(from_attributes=True)
