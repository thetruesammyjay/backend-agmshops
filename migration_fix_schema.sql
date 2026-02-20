-- UPDATED MIGRATION SCRIPT
-- Based on your latest database dump:
-- 1. `users.phone` is already nullable, so we skip it.
-- 2. `stores` is missing 'category' and 'deleted_at'.
-- 3. `products` is missing multiple columns and 'views' needs renaming.
-- 4. `orders` is missing delivery details and 'deleted_at'.

-- 1. Fix Stores Table
ALTER TABLE stores ADD COLUMN category VARCHAR(100) NULL AFTER template_id;
ALTER TABLE stores ADD COLUMN deleted_at DATETIME NULL;
CREATE INDEX idx_stores_deleted_at ON stores(deleted_at);

-- 2. Fix Products Table
ALTER TABLE products ADD COLUMN deleted_at DATETIME NULL;
ALTER TABLE products ADD COLUMN cost_price DECIMAL(12,2) NULL AFTER price;
ALTER TABLE products ADD COLUMN barcode VARCHAR(100) NULL AFTER sku;
ALTER TABLE products ADD COLUMN low_stock_threshold INT NOT NULL DEFAULT 5 AFTER stock_quantity;
ALTER TABLE products ADD COLUMN weight DECIMAL(10,2) NULL;
ALTER TABLE products ADD COLUMN dimensions JSON NULL;
-- Rename 'views' to 'view_count' to match the Python model
ALTER TABLE products CHANGE views view_count INT NOT NULL DEFAULT 0;
CREATE INDEX idx_products_deleted_at ON products(deleted_at);

-- 3. Fix Orders Table
ALTER TABLE orders ADD COLUMN delivery_address TEXT NULL AFTER customer_address;
ALTER TABLE orders ADD COLUMN delivery_state VARCHAR(100) NULL AFTER delivery_address;
ALTER TABLE orders ADD COLUMN delivery_lga VARCHAR(100) NULL AFTER delivery_state;
ALTER TABLE orders ADD COLUMN deleted_at DATETIME NULL;
CREATE INDEX idx_orders_deleted_at ON orders(deleted_at);
