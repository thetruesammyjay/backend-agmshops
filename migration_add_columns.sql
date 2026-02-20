ALTER TABLE users ADD COLUMN deleted_at TIMESTAMP NULL DEFAULT NULL; CREATE INDEX idx_users_deleted_at ON users(deleted_at); ALTER TABLE users ADD COLUMN role VARCHAR(20) DEFAULT 'user' NOT NULL;
