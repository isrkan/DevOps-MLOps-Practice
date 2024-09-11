-- Insert initial expense data if not exists
INSERT INTO expense (amount, category, description, approved, added_by)
SELECT 100.00, 'Travel', 'Flight tickets', true, 'David'
WHERE NOT EXISTS (SELECT 1 FROM expense WHERE id = 1);

INSERT INTO expense (amount, category, description, approved, added_by)
SELECT 50.00, 'Food', 'Dinner', false, 'Ben'
WHERE NOT EXISTS (SELECT 1 FROM expense WHERE id = 2);
