-- Bernalytics Job Counts Table Schema
-- Run this in your Supabase SQL Editor to create the table

-- Create the job_counts table
CREATE TABLE IF NOT EXISTS job_counts (
    id BIGSERIAL PRIMARY KEY,
    collected_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    week_starting DATE NOT NULL,
    location VARCHAR(255) NOT NULL,
    data_engineer INTEGER NOT NULL CHECK (data_engineer >= 0),
    junior_data_engineer INTEGER NOT NULL CHECK (junior_data_engineer >= 0),
    senior_data_engineer INTEGER NOT NULL CHECK (senior_data_engineer >= 0),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    -- Ensure only one record per week per location
    CONSTRAINT unique_week_location UNIQUE (week_starting, location)
);

-- Create index for faster queries by location
CREATE INDEX IF NOT EXISTS idx_job_counts_location ON job_counts(location);

-- Create index for faster queries by week_starting
CREATE INDEX IF NOT EXISTS idx_job_counts_week_starting ON job_counts(week_starting DESC);

-- Create composite index for common queries
CREATE INDEX IF NOT EXISTS idx_job_counts_location_week ON job_counts(location, week_starting DESC);

-- Add updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger to automatically update updated_at
CREATE TRIGGER update_job_counts_updated_at
    BEFORE UPDATE ON job_counts
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Add comments for documentation
COMMENT ON TABLE job_counts IS 'Stores weekly LinkedIn job posting counts for Data Engineering roles';
COMMENT ON COLUMN job_counts.collected_at IS 'Timestamp when the data was collected';
COMMENT ON COLUMN job_counts.week_starting IS 'The Monday of the week being measured';
COMMENT ON COLUMN job_counts.location IS 'Location of the job search (e.g., "Berlin, Germany")';
COMMENT ON COLUMN job_counts.data_engineer IS 'Count for "Data Engineer" search term';
COMMENT ON COLUMN job_counts.junior_data_engineer IS 'Count for "Junior Data Engineer" search term';
COMMENT ON COLUMN job_counts.senior_data_engineer IS 'Count for "Senior Data Engineer" search term';

-- Enable Row Level Security (RLS)
ALTER TABLE job_counts ENABLE ROW LEVEL SECURITY;

-- Create policy to allow all operations for authenticated users
-- Adjust these policies based on your security requirements
CREATE POLICY "Enable read access for all users" ON job_counts
    FOR SELECT USING (true);

CREATE POLICY "Enable insert for authenticated users only" ON job_counts
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Enable update for authenticated users only" ON job_counts
    FOR UPDATE USING (true);

-- Optional: Create a view for the most recent data
CREATE OR REPLACE VIEW recent_job_counts AS
SELECT
    week_starting,
    location,
    data_engineer,
    junior_data_engineer,
    senior_data_engineer,
    collected_at,
    (data_engineer + junior_data_engineer + senior_data_engineer) as total_count
FROM job_counts
ORDER BY week_starting DESC, location
LIMIT 52;  -- Last year of weekly data

COMMENT ON VIEW recent_job_counts IS 'View showing the most recent 52 weeks of job count data';
