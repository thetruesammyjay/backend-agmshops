-- Migration: Add Monnify API alignment fields and new tables
-- Date: 2026-02-06
-- Description: Add transaction_reference and checkout_url to payments table, create disbursements and refunds tables

-- Add new fields to payments table
ALTER TABLE payments 
ADD COLUMN transaction_reference VARCHAR(100) NULL,
ADD COLUMN checkout_url VARCHAR(500) NULL,
ADD INDEX idx_transaction_reference (transaction_reference);

-- Create disbursements table
CREATE TABLE disbursements (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    amount DECIMAL(12, 2) NOT NULL,
    currency VARCHAR(3) NOT NULL DEFAULT 'NGN',
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    reference VARCHAR(100) NOT NULL UNIQUE,
    monnify_reference VARCHAR(100) NULL UNIQUE,
    account_number VARCHAR(20) NOT NULL,
    account_name VARCHAR(255) NOT NULL,
    bank_code VARCHAR(10) NOT NULL,
    bank_name VARCHAR(100) NOT NULL,
    narration VARCHAR(255) NULL,
    fee DECIMAL(12, 2) NULL,
    disbursement_metadata JSON NULL,
    initiated_at DATETIME NOT NULL,
    completed_at DATETIME NULL,
    failed_at DATETIME NULL,
    failure_reason VARCHAR(500) NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NULL ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_user_id (user_id),
    INDEX idx_status (status),
    INDEX idx_reference (reference),
    INDEX idx_monnify_reference (monnify_reference),
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create refunds table
CREATE TABLE refunds (
    id VARCHAR(36) PRIMARY KEY,
    payment_id VARCHAR(36) NOT NULL,
    order_id VARCHAR(36) NOT NULL,
    amount DECIMAL(12, 2) NOT NULL,
    currency VARCHAR(3) NOT NULL DEFAULT 'NGN',
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    refund_reference VARCHAR(100) NOT NULL UNIQUE,
    monnify_reference VARCHAR(100) NULL UNIQUE,
    reason VARCHAR(500) NULL,
    refund_type VARCHAR(20) NOT NULL DEFAULT 'full',
    customer_note VARCHAR(1000) NULL,
    refund_metadata JSON NULL,
    initiated_at DATETIME NOT NULL,
    completed_at DATETIME NULL,
    failed_at DATETIME NULL,
    failure_reason VARCHAR(500) NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NULL ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_payment_id (payment_id),
    INDEX idx_order_id (order_id),
    INDEX idx_status (status),
    INDEX idx_refund_reference (refund_reference),
    INDEX idx_monnify_reference (monnify_reference),
    
    FOREIGN KEY (payment_id) REFERENCES payments(id) ON DELETE CASCADE,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
