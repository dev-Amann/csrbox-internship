-- Supabase SQL Schema for PathEdge

-- Create standard tables for PathEdge
CREATE TABLE IF NOT EXISTS interview_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_name VARCHAR(255) NOT NULL,
    target_role VARCHAR(255) NOT NULL,
    interview_type VARCHAR(100) NOT NULL, -- e.g., 'Resume Review', 'Technical', 'HR'
    feedback_summary TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Note: In the Supabase Dashboard SQL Editor, simply paste and run this code.
-- It will create the necessary table to log mock interview sessions.
