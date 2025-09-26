

-- Index on commonly sorted columns
CREATE INDEX idx_posts_created_date ON posts(created_date DESC);

-- Composite index for filtered pagination
CREATE INDEX idx_posts_category_date ON posts(category, created_date DESC);


-- MySQL: Use covering indexes
SELECT id, title FROM posts ORDER BY created_date LIMIT 10 OFFSET 10000;

-- PostgreSQL: Consider using LIMIT with subqueries
SELECT * FROM posts WHERE id IN (
    SELECT id FROM posts ORDER BY created_date LIMIT 10 OFFSET 10000
);


-- # Standardize on parameter names across your API
-- GET /api/posts?page=2&limit=10
-- # OR
-- GET /api/posts?offset=20&limit=10

