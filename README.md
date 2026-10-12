-- 初始化扩展
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- 1. organizations
CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    type VARCHAR(100) NOT NULL DEFAULT 'company',
    country_code VARCHAR(20),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 2. users
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID REFERENCES organizations(id) ON DELETE SET NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255),
    full_name VARCHAR(255) NOT NULL,
    role_name VARCHAR(100) NOT NULL DEFAULT 'member',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_login_at TIMESTAMPTZ
);

-- 3. roles (可选)
CREATE TABLE roles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 4. projects
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    sponsor_name VARCHAR(255),
    study_type VARCHAR(100) NOT NULL DEFAULT 'interventional',
    status VARCHAR(100) NOT NULL DEFAULT 'draft',
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

ALTER TABLE projects
  ADD CONSTRAINT chk_projects_status CHECK (status IN ('draft','active','in_review','approved','archived'));

-- 5. project_members
CREATE TABLE project_members (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role_id UUID REFERENCES roles(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(project_id, user_id)
);

-- 6. study_basics (1:1 with project)
CREATE TABLE study_basics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL UNIQUE REFERENCES projects(id) ON DELETE CASCADE,
    indication VARCHAR(500) NOT NULL,
    phase VARCHAR(50) NOT NULL,
    population_description TEXT,
    intervention_name VARCHAR(255),
    comparator_name VARCHAR(255),
    blinding_method VARCHAR(100),
    randomization_method VARCHAR(150),
    study_duration_weeks INTEGER,
    target_sample_size INTEGER,
    expected_dropout_rate NUMERIC(5,2),
    primary_objective TEXT,
    secondary_objectives TEXT,
    primary_endpoint TEXT,
    secondary_endpoints TEXT,
    safety_focus TEXT,
    study_aims TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 7. study_designs (1:1 可选)
CREATE TABLE study_designs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL UNIQUE REFERENCES projects(id) ON DELETE CASCADE,
    design_type VARCHAR(100) NOT NULL,
    allocation_ratio VARCHAR(50),
    treatment_duration_weeks INTEGER,
    follow_up_weeks INTEGER,
    inclusion_summary TEXT,
    exclusion_summary TEXT,
    number_of_arms INTEGER,
    is_therapeutic BOOLEAN DEFAULT FALSE,
    is_interventional BOOLEAN DEFAULT TRUE,
    is_randomized BOOLEAN DEFAULT FALSE,
    is_blinded BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 8. inclusion_exclusion
CREATE TABLE inclusion_exclusion (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    criterion_type VARCHAR(30) NOT NULL,
    criterion_text TEXT NOT NULL,
    sort_order INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(project_id, criterion_type, sort_order)
);

-- 9. interventions
CREATE TABLE interventions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    arm_name VARCHAR(255) NOT NULL,
    description TEXT,
    dose_regimen TEXT,
    route VARCHAR(100),
    schedule TEXT,
    comparator_flag BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 10. endpoints
CREATE TABLE endpoints (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    endpoint_type VARCHAR(50) NOT NULL,
    name VARCHAR(255) NOT NULL,
    definition TEXT,
    measurement_timepoint VARCHAR(255),
    analysis_method VARCHAR(255),
    sort_order INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 11. sample_size_inputs
CREATE TABLE sample_size_inputs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    alpha NUMERIC(5,4),
    power NUMERIC(5,4),
    effect_size NUMERIC(10,4),
    standard_deviation NUMERIC(10,4),
    dropout_rate NUMERIC(5,2),
    allocation_ratio NUMERIC(10,4),
    method_type VARCHAR(100),
    assumptions TEXT,
    result_total INTEGER,
    result_per_group INTEGER,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 12. protocol_versions
CREATE TABLE protocol_versions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    version_number VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    status VARCHAR(100) NOT NULL DEFAULT 'draft',
    created_by UUID REFERENCES users(id),
    approved_by UUID REFERENCES users(id),
    approved_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(project_id, version_number)
);

ALTER TABLE protocol_versions
  ADD CONSTRAINT chk_protocol_versions_status CHECK (status IN ('draft','in_review','revisions_needed','approved','archived'));

-- 13. protocol_sections
CREATE TABLE protocol_sections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    version_id UUID NOT NULL REFERENCES protocol_versions(id) ON DELETE CASCADE,
    section_code VARCHAR(100) NOT NULL,
    section_title VARCHAR(255) NOT NULL,
    content TEXT,
    is_generated BOOLEAN NOT NULL DEFAULT TRUE,
    generation_model VARCHAR(255),
    source_reference TEXT,
    revision_count INTEGER NOT NULL DEFAULT 0,
    last_modified_by UUID REFERENCES users(id),
    confidence_score NUMERIC(5,4),
    needs_human_review BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(version_id, section_code)
);

-- 14. review_comments
CREATE TABLE review_comments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    version_id UUID NOT NULL REFERENCES protocol_versions(id) ON DELETE CASCADE,
    section_id UUID REFERENCES protocol_sections(id) ON DELETE SET NULL,
    reviewer_user_id UUID NOT NULL REFERENCES users(id),
    comment TEXT NOT NULL,
    severity VARCHAR(50) NOT NULL DEFAULT 'medium',
    status VARCHAR(50) NOT NULL DEFAULT 'open',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

ALTER TABLE review_comments
  ADD CONSTRAINT chk_review_comments_severity CHECK (severity IN ('low','medium','high'));

-- 15. validation_results
CREATE TABLE validation_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    version_id UUID NOT NULL REFERENCES protocol_versions(id) ON DELETE CASCADE,
    rule_code VARCHAR(100) NOT NULL,
    rule_name VARCHAR(255) NOT NULL,
    severity VARCHAR(50) NOT NULL DEFAULT 'medium',
    passed BOOLEAN NOT NULL DEFAULT FALSE,
    message TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 16. source_documents
CREATE TABLE source_documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    storage_path VARCHAR(500) NOT NULL,
    file_hash VARCHAR(128),
    source_type VARCHAR(50) DEFAULT 'uploaded',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 17. guideline_documents
CREATE TABLE guideline_documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    version VARCHAR(50),
    source_url TEXT,
    content TEXT,
    metadata JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 18. guideline_chunks (用于 RAG，embedding 存 JSONB)
CREATE TABLE guideline_chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    guideline_id UUID REFERENCES guideline_documents(id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    chunk_text TEXT NOT NULL,
    embedding JSONB, -- 存向量数组或其它 metadata
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 19. prompt_logs
CREATE TABLE prompt_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id) ON DELETE SET NULL,
    version_id UUID REFERENCES protocol_versions(id) ON DELETE SET NULL,
    section_code VARCHAR(100),
    prompt_text TEXT NOT NULL,
    model_name VARCHAR(255),
    response_text TEXT,
    tokens_in INTEGER,
    tokens_out INTEGER,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 20. audit_logs
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id) ON DELETE SET NULL,
    version_id UUID REFERENCES protocol_versions(id) ON DELETE SET NULL,
    user_id UUID REFERENCES users(id),
    action_type VARCHAR(100) NOT NULL,
    entity_type VARCHAR(100),
    entity_id UUID,
    details JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 21. exports
CREATE TABLE exports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    version_id UUID NOT NULL REFERENCES protocol_versions(id) ON DELETE CASCADE,
    export_type VARCHAR(50) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    generated_by UUID REFERENCES users(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 22. tasks (异步任务)
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id) ON DELETE SET NULL,
    version_id UUID REFERENCES protocol_versions(id) ON DELETE SET NULL,
    task_name VARCHAR(255) NOT NULL,
    status VARCHAR(100) NOT NULL DEFAULT 'queued',
    payload JSONB,
    result JSONB,
    error_message TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 23. version_snapshots (可选)
CREATE TABLE version_snapshots (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    version_id UUID NOT NULL REFERENCES protocol_versions(id) ON DELETE CASCADE,
    snapshot_label VARCHAR(100),
    section_json JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 索引
CREATE INDEX idx_users_organization_id ON users(organization_id);
CREATE INDEX idx_project_members_project_id ON project_members(project_id);
CREATE INDEX idx_project_members_user_id ON project_members(user_id);
CREATE INDEX idx_projects_organization_id ON projects(organization_id);
CREATE INDEX idx_projects_status ON projects(status);
CREATE INDEX idx_study_basics_project_id ON study_basics(project_id);
CREATE INDEX idx_study_designs_project_id ON study_designs(project_id);
CREATE INDEX idx_inclusion_exclusion_project_id ON inclusion_exclusion(project_id);
CREATE INDEX idx_interventions_project_id ON interventions(project_id);
CREATE INDEX idx_endpoints_project_id ON endpoints(project_id);
CREATE INDEX idx_sample_size_inputs_project_id ON sample_size_inputs(project_id);
CREATE INDEX idx_protocol_versions_project_id ON protocol_versions(project_id);
CREATE INDEX idx_protocol_sections_version_id ON protocol_sections(version_id);
CREATE INDEX idx_review_comments_version_id ON review_comments(version_id);
CREATE INDEX idx_validation_results_version_id ON validation_results(version_id);
CREATE INDEX idx_audit_logs_project_id ON audit_logs(project_id);
CREATE INDEX idx_audit_logs_version_id ON audit_logs(version_id);
CREATE INDEX idx_prompt_logs_version_id ON prompt_logs(version_id);

-- 示例触发器/更新时间（可选）：自动更新 updated_at
CREATE OR REPLACE FUNCTION trigger_set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 给常用表添加触发器
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_trigger WHERE tgname = 'projects_set_updated_at'
  ) THEN
    CREATE TRIGGER projects_set_updated_at
    BEFORE UPDATE ON projects
    FOR EACH ROW EXECUTE FUNCTION trigger_set_updated_at();
  END IF;
END;
$$;

DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_trigger WHERE tgname = 'protocol_versions_set_updated_at'
  ) THEN
    CREATE TRIGGER protocol_versions_set_updated_at
    BEFORE UPDATE ON protocol_versions
    FOR EACH ROW EXECUTE FUNCTION trigger_set_updated_at();
  END IF;
END;
$$;

-- 结束
