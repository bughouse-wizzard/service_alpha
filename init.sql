-- Initialize database for Service Alpha

-- Create items table
CREATE TABLE IF NOT EXISTS items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create tasks table for Celery results (optional)
CREATE TABLE IF NOT EXISTS celery_tasks (
    id VARCHAR(255) PRIMARY KEY,
    status VARCHAR(50) NOT NULL,
    result JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

-- Insert sample data
INSERT INTO items (name, description) VALUES
    ('Sample Item 1', 'This is the first sample item'),
    ('Sample Item 2', 'This is the second sample item'),
    ('Sample Item 3', 'This is the third sample item')
ON CONFLICT (id) DO NOTHING;

-- Create index for better performance
CREATE INDEX IF NOT EXISTS idx_items_created_at ON items(created_at);
CREATE INDEX IF NOT EXISTS idx_celery_tasks_status ON celery_tasks(status);