-- ============================================================
-- AGM Store Builder - TiDB Cloud Compatible Schema
-- Generated from FastAPI/SQLAlchemy models
-- Compatible with: TiDB Cloud (MySQL 8.0 dialect)
--
-- HOW TO USE:
--   1. Open TiDB Cloud → SQL Editor
--   2. Select your database (agm_store_builder) from the dropdown
--   3. Paste this entire file and click Run
-- ============================================================

-- ============================================================
-- TABLE: users
-- ============================================================
CREATE TABLE `users` (
  `id`                        VARCHAR(36)  NOT NULL,
  `email`                     VARCHAR(255) NOT NULL,
  `password_hash`             VARCHAR(255) NOT NULL,
  `full_name`                 VARCHAR(255) NOT NULL,
  `phone`                     VARCHAR(20)  DEFAULT NULL,
  `avatar_url`                VARCHAR(500) DEFAULT NULL,
  `role`                      VARCHAR(20)  NOT NULL DEFAULT 'user',
  `email_verified`            TINYINT(1)   NOT NULL DEFAULT 0,
  `phone_verified`            TINYINT(1)   NOT NULL DEFAULT 0,
  `is_active`                 TINYINT(1)   NOT NULL DEFAULT 1,
  `has_completed_onboarding`  TINYINT(1)   NOT NULL DEFAULT 0,
  `last_login_at`             DATETIME     DEFAULT NULL,
  `created_at`                DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at`                DATETIME     DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at`                DATETIME     DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_users_email`  (`email`),
  UNIQUE KEY `uq_users_phone`  (`phone`),
  KEY `ix_users_email`         (`email`),
  KEY `ix_users_phone`         (`phone`),
  KEY `ix_users_deleted_at`    (`deleted_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ============================================================
-- TABLE: user_settings
-- ============================================================
CREATE TABLE `user_settings` (
  `id`                      VARCHAR(36)  NOT NULL,
  `user_id`                 VARCHAR(36)  NOT NULL,
  `email_notifications`     TINYINT(1)   NOT NULL DEFAULT 1,
  `sms_notifications`       TINYINT(1)   NOT NULL DEFAULT 1,
  `order_notifications`     TINYINT(1)   NOT NULL DEFAULT 1,
  `payment_notifications`   TINYINT(1)   NOT NULL DEFAULT 1,
  `payout_notifications`    TINYINT(1)   NOT NULL DEFAULT 1,
  `marketing_notifications` TINYINT(1)   NOT NULL DEFAULT 0,
  `profile_visibility`      VARCHAR(20)  NOT NULL DEFAULT 'public',
  `show_email`              TINYINT(1)   NOT NULL DEFAULT 0,
  `show_phone`              TINYINT(1)   NOT NULL DEFAULT 0,
  `default_currency`        VARCHAR(3)   NOT NULL DEFAULT 'NGN',
  `timezone`                VARCHAR(50)  NOT NULL DEFAULT 'Africa/Lagos',
  `language`                VARCHAR(10)  NOT NULL DEFAULT 'en',
  `two_factor_enabled`      TINYINT(1)   NOT NULL DEFAULT 0,
  `login_alerts`            TINYINT(1)   NOT NULL DEFAULT 1,
  `created_at`              DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at`              DATETIME     DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_user_settings_user_id` (`user_id`),
  KEY `ix_user_settings_user_id` (`user_id`),
  CONSTRAINT `fk_user_settings_user_id`
    FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ============================================================
-- TABLE: refresh_tokens
-- ============================================================
CREATE TABLE `refresh_tokens` (
  `id`          VARCHAR(36)  NOT NULL,
  `user_id`     VARCHAR(36)  NOT NULL,
  `token_hash`  VARCHAR(255) NOT NULL,
  `expires_at`  DATETIME     NOT NULL,
  `revoked`     TINYINT(1)   NOT NULL DEFAULT 0,
  `revoked_at`  DATETIME     DEFAULT NULL,
  `created_at`  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `ix_refresh_tokens_user_id`    (`user_id`),
  KEY `ix_refresh_tokens_token_hash` (`token_hash`),
  KEY `ix_refresh_tokens_expires_at` (`expires_at`),
  KEY `ix_refresh_tokens_revoked`    (`revoked`),
  CONSTRAINT `fk_refresh_tokens_user_id`
    FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ============================================================
-- TABLE: otp_verifications
-- ============================================================
CREATE TABLE `otp_verifications` (
  `id`         VARCHAR(36)  NOT NULL,
  `email`      VARCHAR(255) DEFAULT NULL,
  `phone`      VARCHAR(20)  DEFAULT NULL,
  `code`       VARCHAR(6)   NOT NULL,
  `otp_type`   VARCHAR(20)  NOT NULL,
  `verified`   TINYINT(1)   NOT NULL DEFAULT 0,
  `expires_at` DATETIME     NOT NULL,
  `created_at` DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `ix_otp_verifications_email`      (`email`),
  KEY `ix_otp_verifications_phone`      (`phone`),
  KEY `ix_otp_verifications_code`       (`code`),
  KEY `ix_otp_verifications_otp_type`   (`otp_type`),
  KEY `ix_otp_verifications_verified`   (`verified`),
  KEY `ix_otp_verifications_expires_at` (`expires_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ============================================================
-- TABLE: bank_accounts
-- ============================================================
CREATE TABLE `bank_accounts` (
  `id`             VARCHAR(36)  NOT NULL,
  `user_id`        VARCHAR(36)  NOT NULL,
  `account_number` VARCHAR(20)  NOT NULL,
  `account_name`   VARCHAR(255) NOT NULL,
  `bank_code`      VARCHAR(10)  NOT NULL,
  `bank_name`      VARCHAR(255) NOT NULL,
  `is_verified`    TINYINT(1)   NOT NULL DEFAULT 0,
  `is_primary`     TINYINT(1)   NOT NULL DEFAULT 0,
  `created_at`     DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at`     DATETIME     DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_account` (`user_id`, `account_number`, `bank_code`),
  KEY `ix_bank_accounts_user_id`        (`user_id`),
  KEY `ix_bank_accounts_account_number` (`account_number`),
  KEY `ix_bank_accounts_bank_code`      (`bank_code`),
  CONSTRAINT `fk_bank_accounts_user_id`
    FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ============================================================
-- TABLE: stores
-- ============================================================
CREATE TABLE `stores` (
  `id`            VARCHAR(36)  NOT NULL,
  `user_id`       VARCHAR(36)  NOT NULL,
  `username`      VARCHAR(100) NOT NULL,
  `display_name`  VARCHAR(255) NOT NULL,
  `description`   TEXT         DEFAULT NULL,
  `logo_url`      VARCHAR(500) DEFAULT NULL,
  `banner_url`    VARCHAR(500) DEFAULT NULL,
  `template_id`   VARCHAR(20)  NOT NULL DEFAULT 'products',
  `category`      VARCHAR(100) DEFAULT NULL,
  `custom_colors` JSON         DEFAULT NULL,
  `custom_fonts`  JSON         DEFAULT NULL,
  `social_links`  JSON         DEFAULT NULL,
  `is_active`     TINYINT(1)   NOT NULL DEFAULT 1,
  `created_at`    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at`    DATETIME     DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at`    DATETIME     DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_stores_username` (`username`),
  KEY `ix_stores_user_id`    (`user_id`),
  KEY `ix_stores_username`   (`username`),
  KEY `ix_stores_category`   (`category`),
  KEY `ix_stores_is_active`  (`is_active`),
  KEY `ix_stores_deleted_at` (`deleted_at`),
  CONSTRAINT `fk_stores_user_id`
    FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ============================================================
-- TABLE: products
-- ============================================================
CREATE TABLE `products` (
  `id`                  VARCHAR(36)    NOT NULL,
  `store_id`            VARCHAR(36)    NOT NULL,
  `name`                VARCHAR(255)   NOT NULL,
  `description`         TEXT           DEFAULT NULL,
  `price`               DECIMAL(12, 2) NOT NULL,
  `compare_at_price`    DECIMAL(12, 2) DEFAULT NULL,
  `cost_price`          DECIMAL(12, 2) DEFAULT NULL,
  `sku`                 VARCHAR(100)   DEFAULT NULL,
  `barcode`             VARCHAR(100)   DEFAULT NULL,
  `stock_quantity`      INT            NOT NULL DEFAULT 0,
  `low_stock_threshold` INT            NOT NULL DEFAULT 5,
  `weight`              DECIMAL(10, 2) DEFAULT NULL,
  `dimensions`          JSON           DEFAULT NULL,
  `images`              JSON           NOT NULL,
  `variations`          JSON           DEFAULT NULL,
  `category`            VARCHAR(100)   DEFAULT NULL,
  `tags`                JSON           DEFAULT NULL,
  `is_active`           TINYINT(1)     NOT NULL DEFAULT 1,
  `is_featured`         TINYINT(1)     NOT NULL DEFAULT 0,
  `view_count`          INT            NOT NULL DEFAULT 0,
  `created_at`          DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at`          DATETIME       DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at`          DATETIME       DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_products_store_id`      (`store_id`),
  KEY `ix_products_sku`           (`sku`),
  KEY `ix_products_stock_quantity`(`stock_quantity`),
  KEY `ix_products_category`      (`category`),
  KEY `ix_products_is_active`     (`is_active`),
  KEY `ix_products_is_featured`   (`is_featured`),
  KEY `ix_products_deleted_at`    (`deleted_at`),
  CONSTRAINT `fk_products_store_id`
    FOREIGN KEY (`store_id`) REFERENCES `stores` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ============================================================
-- TABLE: orders
-- ============================================================
CREATE TABLE `orders` (
  `id`               VARCHAR(36)    NOT NULL,
  `store_id`         VARCHAR(36)    NOT NULL,
  `order_number`     VARCHAR(50)    NOT NULL,
  `customer_name`    VARCHAR(255)   NOT NULL,
  `customer_email`   VARCHAR(255)   DEFAULT NULL,
  `customer_phone`   VARCHAR(20)    NOT NULL,
  `customer_address` JSON           DEFAULT NULL,
  `delivery_address` TEXT           DEFAULT NULL,
  `delivery_state`   VARCHAR(100)   DEFAULT NULL,
  `delivery_lga`     VARCHAR(100)   DEFAULT NULL,
  `items`            JSON           NOT NULL,
  `subtotal`         DECIMAL(12, 2) NOT NULL,
  `discount`         DECIMAL(12, 2) NOT NULL DEFAULT 0.00,
  `shipping_fee`     DECIMAL(12, 2) NOT NULL DEFAULT 0.00,
  `agm_fee`          DECIMAL(12, 2) NOT NULL DEFAULT 0.00,
  `total`            DECIMAL(12, 2) NOT NULL,
  `status`           VARCHAR(20)    NOT NULL DEFAULT 'pending',
  `payment_status`   VARCHAR(20)    NOT NULL DEFAULT 'pending',
  `notes`            TEXT           DEFAULT NULL,
  `created_at`       DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at`       DATETIME       DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at`       DATETIME       DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_orders_order_number` (`order_number`),
  KEY `ix_orders_store_id`       (`store_id`),
  KEY `ix_orders_order_number`   (`order_number`),
  KEY `ix_orders_customer_email` (`customer_email`),
  KEY `ix_orders_customer_phone` (`customer_phone`),
  KEY `ix_orders_status`         (`status`),
  KEY `ix_orders_payment_status` (`payment_status`),
  KEY `ix_orders_deleted_at`     (`deleted_at`),
  CONSTRAINT `fk_orders_store_id`
    FOREIGN KEY (`store_id`) REFERENCES `stores` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ============================================================
-- TABLE: payments
-- ============================================================
CREATE TABLE `payments` (
  `id`                    VARCHAR(36)    NOT NULL,
  `order_id`              VARCHAR(36)    NOT NULL,
  `amount`                DECIMAL(12, 2) NOT NULL,
  `currency`              VARCHAR(3)     NOT NULL DEFAULT 'NGN',
  `status`                VARCHAR(20)    NOT NULL DEFAULT 'pending',
  `payment_method`        VARCHAR(20)    DEFAULT NULL,
  `payment_reference`     VARCHAR(100)   NOT NULL,
  `monnify_reference`     VARCHAR(100)   DEFAULT NULL,
  `transaction_reference` VARCHAR(100)   DEFAULT NULL,
  `checkout_url`          VARCHAR(500)   DEFAULT NULL,
  `account_number`        VARCHAR(20)    DEFAULT NULL,
  `account_name`          VARCHAR(255)   DEFAULT NULL,
  `bank_name`             VARCHAR(100)   DEFAULT NULL,
  `payment_metadata`      JSON           DEFAULT NULL,
  `paid_at`               DATETIME       DEFAULT NULL,
  `expires_at`            DATETIME       DEFAULT NULL,
  `created_at`            DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at`            DATETIME       DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_payments_payment_reference`  (`payment_reference`),
  UNIQUE KEY `uq_payments_monnify_reference`  (`monnify_reference`),
  KEY `ix_payments_order_id`              (`order_id`),
  KEY `ix_payments_status`                (`status`),
  KEY `ix_payments_payment_reference`     (`payment_reference`),
  KEY `ix_payments_monnify_reference`     (`monnify_reference`),
  KEY `ix_payments_transaction_reference` (`transaction_reference`),
  CONSTRAINT `fk_payments_order_id`
    FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ============================================================
-- TABLE: refunds
-- ============================================================
CREATE TABLE `refunds` (
  `id`                VARCHAR(36)    NOT NULL,
  `payment_id`        VARCHAR(36)    NOT NULL,
  `order_id`          VARCHAR(36)    NOT NULL,
  `amount`            DECIMAL(12, 2) NOT NULL,
  `currency`          VARCHAR(3)     NOT NULL DEFAULT 'NGN',
  `status`            VARCHAR(20)    NOT NULL DEFAULT 'pending',
  `refund_reference`  VARCHAR(100)   NOT NULL,
  `monnify_reference` VARCHAR(100)   DEFAULT NULL,
  `reason`            VARCHAR(500)   DEFAULT NULL,
  `refund_type`       VARCHAR(20)    NOT NULL DEFAULT 'full',
  `customer_note`     VARCHAR(1000)  DEFAULT NULL,
  `refund_metadata`   JSON           DEFAULT NULL,
  `initiated_at`      DATETIME       NOT NULL,
  `completed_at`      DATETIME       DEFAULT NULL,
  `failed_at`         DATETIME       DEFAULT NULL,
  `failure_reason`    VARCHAR(500)   DEFAULT NULL,
  `created_at`        DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at`        DATETIME       DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_refunds_refund_reference`  (`refund_reference`),
  UNIQUE KEY `uq_refunds_monnify_reference` (`monnify_reference`),
  KEY `ix_refunds_payment_id`        (`payment_id`),
  KEY `ix_refunds_order_id`          (`order_id`),
  KEY `ix_refunds_status`            (`status`),
  KEY `ix_refunds_refund_reference`  (`refund_reference`),
  KEY `ix_refunds_monnify_reference` (`monnify_reference`),
  CONSTRAINT `fk_refunds_payment_id`
    FOREIGN KEY (`payment_id`) REFERENCES `payments` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_refunds_order_id`
    FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ============================================================
-- TABLE: disbursements
-- ============================================================
CREATE TABLE `disbursements` (
  `id`                      VARCHAR(36)    NOT NULL,
  `user_id`                 VARCHAR(36)    NOT NULL,
  `amount`                  DECIMAL(12, 2) NOT NULL,
  `currency`                VARCHAR(3)     NOT NULL DEFAULT 'NGN',
  `status`                  VARCHAR(20)    NOT NULL DEFAULT 'pending',
  `reference`               VARCHAR(100)   NOT NULL,
  `monnify_reference`       VARCHAR(100)   DEFAULT NULL,
  `account_number`          VARCHAR(20)    NOT NULL,
  `account_name`            VARCHAR(255)   NOT NULL,
  `bank_code`               VARCHAR(10)    NOT NULL,
  `bank_name`               VARCHAR(100)   NOT NULL,
  `narration`               VARCHAR(255)   DEFAULT NULL,
  `fee`                     DECIMAL(12, 2) DEFAULT NULL,
  `disbursement_metadata`   JSON           DEFAULT NULL,
  `initiated_at`            DATETIME       NOT NULL,
  `completed_at`            DATETIME       DEFAULT NULL,
  `failed_at`               DATETIME       DEFAULT NULL,
  `failure_reason`          VARCHAR(500)   DEFAULT NULL,
  `created_at`              DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at`              DATETIME       DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_disbursements_reference`         (`reference`),
  UNIQUE KEY `uq_disbursements_monnify_reference` (`monnify_reference`),
  KEY `ix_disbursements_user_id`          (`user_id`),
  KEY `ix_disbursements_status`           (`status`),
  KEY `ix_disbursements_reference`        (`reference`),
  KEY `ix_disbursements_monnify_reference`(`monnify_reference`),
  CONSTRAINT `fk_disbursements_user_id`
    FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ============================================================
-- END OF SCHEMA
-- ============================================================
