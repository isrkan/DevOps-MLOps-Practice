-- Create table for expenses
CREATE TABLE IF NOT EXISTS expense (
    id SERIAL PRIMARY KEY,
    amount DECIMAL(10, 2),
    category VARCHAR(255),
    description VARCHAR(255),
    approved BOOLEAN,
    added_by VARCHAR(255)
);