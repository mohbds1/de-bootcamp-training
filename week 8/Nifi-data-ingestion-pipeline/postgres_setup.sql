CREATE TABLE db_transactions (
    id SERIAL PRIMARY KEY,
    user_id INT,
    amount VARCHAR(50),
    status VARCHAR(50),
    category VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO db_transactions (user_id, amount, status, category) VALUES 
(101, '250.50', 'Active', 'Electronics'),
(102, 'INVALID', '???', 'Books'),        
(103, '100.00', 'Pending', 'Clothing'),
(104, NULL, 'Failed', 'Food'),      
(105, '500.75', 'Active', 'Electronics');


Select * from db_transactions;