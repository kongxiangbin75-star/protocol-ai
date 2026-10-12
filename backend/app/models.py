import uuid
from sqlalchemy import (
    Boolean, Column, DateTime, ForeignKey, Integer, JSON, Numeric, String, Text, UniqueConstraint
)
from sqlalchemy.sql import func

from app.database import Base

def gen_uuid():
    return str(uuid.uuid4())

class Organization(Base):
    __tablename__ = "organizations"
    id = Column(String(36), primary_key=True, default=gen_uuid)
    name = Column(String(255), nullable=False)
    type = Column(String(100), nullable=False, default="company")
    country_code = Column(String(20), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class User(Base):
    __tablename__ = "users"
    id = Column(String(36), primary_key=True, default=gen_uuid)
    organization_id = Column(String(36), ForeignKey("organizations.id", ondelete="SET NULL"))
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=True)
    full_name = Column(String(255), nullable=False)
    role_name = Column(String(100), nullable=False, default="member")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    last_login_at = Column(DateTime(timezone=True), nullable=True)

class Role(Base):
    __tablename__ = "roles"
    id = Column(String(36), primary_key=True, default=gen_uuid)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Project(Base):
    __tablename__ = "projects"
    id = Column(String(36), primary_key=True, default=gen_uuid)
    organization_id = Column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"))
    name = Column(String(255), nullable=False)
    sponsor_name = Column(String(255), nullable=True)
    study_type = Column(String(100), nullable=False, default="interventional")
    status = Column(String(100), nullable=False, default="draft")
    created_by = Column(String(36), ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class ProjectMember(Base):
    __tablename__ = "project_members"
    id = Column(String(36), primary_key=True, default=gen_uuid)
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role_id = Column(String(36), ForeignKey("roles.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    __table_args__ = (UniqueConstraint("project_id", "user_id", name="uq_project_member"),)

class StudyBasic(Base):
    __tablename__ = "study_basics"
    id = Column(String(36), primary_key=True, default=gen_uuid)
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), unique=True, nullable=False)
    indication = Column(String(500), nullable=False)
    phase = Column(String(50), nullable=False)
    population_description = Column(Text)
    intervention_name = Column(String(255))
    comparator_name = Column(String(255))
    blinding_method = Column(String(100))
    randomization_method = Column(String(150))
    study_duration_weeks = Column(Integer)
    target_sample_size = Column(Integer)
    expected_dropout_rate = Column(Numeric(5, 2))
    primary_objective = Column(Text)
    secondary_objectives = Column(Text)
    primary_endpoint = Column(Text)
    secondary_endpoints = Column(Text)
    safety_focus = Column(Text)
    study_aims = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class StudyDesign(Base):
    __tablename__ = "study_designs"
    id = Column(String(36), primary_key=True, default=gen_uuid)
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), unique=True, nullable=False)
    design_type = Column(String(100), nullable=False)
    allocation_ratio = Column(String(50))
    treatment_duration_weeks = Column(Integer)
    follow_up_weeks = Column(Integer)
    inclusion_summary = Column(Text)
    exclusion_summary = Column(Text)
    number_of_arms = Column(Integer)
    is_therapeutic = Column(Boolean, default=False)
    is_interventional = Column(Boolean, default=True)
    is_randomized = Column(Boolean, default=False)
    is_blinded = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class InclusionExclusion(Base):
    __tablename__ = "inclusion_exclusion"
    id = Column(String(36), primary_key=True, default=gen_uuid)
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    criterion_type = Column(String(30), nullable=False)
    criterion_text = Column(Text, nullable=False)
    sort_order = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    __table_args__ = (UniqueConstraint("project_id", "criterion_type", "sort_order", name="uq_project_criterion_order"),)

class Intervention(Base):
    __tablename__ = "interventions"
    id = Column(String(36), primary_key=True, default=gen_uuid)
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    arm_name = Column(String(255), nullable=False)
    description = Column(Text)
    dose_regimen = Column(Text)
    route = Column(String(100))
    schedule = Column(Text)
    comparator_flag = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Endpoint(Base):
    __tablename__ = "endpoints"
    id = Column(String(36), primary_key=True, default=gen_uuid)
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    endpoint_type = Column(String(50), nullable=False)
    name = Column(String(255), nullable=False)
    definition = Column(Text)
    measurement_timepoint = Column(String(255))
    analysis_method = Column(String(255))
    sort_order = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class SampleSizeInput(Base):
    __tablename__ = "sample_size_inputs"
    id = Column(String(36), primary_key=True, default=gen_uuid)
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    alpha = Column(Numeric(5, 4))
    power = Column(Numeric(5, 4))
    effect_size = Column(Numeric(10, 4))
    standard_deviation = Column(Numeric(10, 4))
    dropout_rate = Column(Numeric(5, 2))
    allocation_ratio = Column(Numeric(10, 4))
    method_type = Column(String(100))
    assumptions = Column(Text)
    result_total = Column(Integer)
    result_per_group = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ProtocolVersion(Base):
    __tablename__ = "protocol_versions"
    id = Column(String(36), primary_key=True, default=gen_uuid)
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    version_number = Column(String(50), nullable=False)
    title = Column(String(255), nullable=False)
    status = Column(String(100), nullable=False, default="draft")
    created_by = Column(String(36), ForeignKey("users.id"))
    approved_by = Column(String(36), ForeignKey("users.id"))
    approved_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    __table_args__ = (UniqueConstraint("project_id", "version_number", name="uq_project_version"),)

class ProtocolSection(Base):
    __tablename__ = "protocol_sections"
    id = Column(String(36), primary_key=True, default=gen_uuid)
    version_id = Column(String(36), ForeignKey("protocol_versions.id", ondelete="CASCADE"), nullable=False)
    section_code = Column(String(100), nullable=False)
    section_title = Column(String(255), nullable=False)
    content = Column(Text)
    is_generated = Column(Boolean, default=True)
    generation_model = Column(String(255))
    source_reference = Column(Text)
    revision_count = Column(Integer, default=0)
    last_modified_by = Column(String(36), ForeignKey("users.id"))
    confidence_score = Column(Numeric(5, 4))
    needs_human_review = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    __table_args__ = (UniqueConstraint("version_id", "section_code", name="uq_version_section"),)

class ReviewComment(Base):
    __tablename__ = "review_comments"
    id = Column(String(36), primary_key=True, default=gen_uuid)
    version_id = Column(String(36), ForeignKey("protocol_versions.id", ondelete="CASCADE"), nullable=False)
    section_id = Column(String(36), ForeignKey("protocol_sections.id", ondelete="SET NULL"), nullable=True)
    reviewer_user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    comment = Column(Text, nullable=False)
    severity = Column(String(50), nullable=False, default="medium")
    status = Column(String(50), nullable=False, default="open")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ValidationResult(Base):
    __tablename__ = "validation_results"
    id = Column(String(36), primary_key=True, default=gen_uuid)
    version_id = Column(String(36), ForeignKey("protocol_versions.id", ondelete="CASCADE"), nullable=False)
    rule_code = Column(String(100), nullable=False)
    rule_name = Column(String(255), nullable=False)
    severity = Column(String(50), nullable=False, default="medium")
    passed = Column(Boolean, default=False)
    message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class SourceDocument(Base):
    __tablename__ = "source_documents"
    id = Column(String(36), primary_key=True, default=gen_uuid)
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=True)
    title = Column(String(255), nullable=False)
    category = Column(String(100))
    storage_path = Column(String(500), nullable=False)
    file_hash = Column(String(128))
    source_type = Column(String(50), default="uploaded")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class GuidelineDocument(Base):
    __tablename__ = "guideline_documents"
    id = Column(String(36), primary_key=True, default=gen_uuid)
    title = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    version = Column(String(50))
    source_url = Column(Text)
    content = Column(Text)
    metadata = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class GuidelineChunk(Base):
    __tablename__ = "guideline_chunks"
    id = Column(String(36), primary_key=True, default=gen_uuid)
    guideline_id = Column(String(36), ForeignKey("guideline_documents.id", ondelete="CASCADE"))
    chunk_index = Column(Integer, nullable=False)
    chunk_text = Column(Text, nullable=False)
    embedding = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class PromptLog(Base):
    __tablename__ = "prompt_logs"
    id = Column(String(36), primary_key=True, default=gen_uuid)
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="SET NULL"), nullable=True)
    version_id = Column(String(36), ForeignKey("protocol_versions.id", ondelete="SET NULL"), nullable=True)
    section_code = Column(String(100))
    prompt_text = Column(Text, nullable=False)
    model_name = Column(String(255))
    response_text = Column(Text)
    tokens_in = Column(Integer)
    tokens_out = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(String(36), primary_key=True, default=gen_uuid)
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="SET NULL"), nullable=True)
    version_id = Column(String(36), ForeignKey("protocol_versions.id", ondelete="SET NULL"), nullable=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    action_type = Column(String(100), nullable=False)
    entity_type = Column(String(100))
    entity_id = Column(String(36))
    details = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ExportRecord(Base):
    __tablename__ = "exports"
    id = Column(String(36), primary_key=True, default=gen_uuid)
    version_id = Column(String(36), ForeignKey("protocol_versions.id", ondelete="CASCADE"), nullable=False)
    export_type = Column(String(50), nullable=False)
    file_path = Column(String(500), nullable=False)
    generated_by = Column(String(36), ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class TaskRecord(Base):
    __tablename__ = "tasks"
    id = Column(String(36), primary_key=True, default=gen_uuid)
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="SET NULL"), nullable=True)
    version_id = Column(String(36), ForeignKey("protocol_versions.id", ondelete="SET NULL"), nullable=True)
    task_name = Column(String(255), nullable=False)
    status = Column(String(100), nullable=False, default="queued")
    payload = Column(JSON)
    result = Column(JSON)
    error_message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class VersionSnapshot(Base):
    __tablename__ = "version_snapshots"
    id = Column(String(36), primary_key=True, default=gen_uuid)
    version_id = Column(String(36), ForeignKey("protocol_versions.id", ondelete="CASCADE"), nullable=False)
    snapshot_label = Column(String(100))
    section_json = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
