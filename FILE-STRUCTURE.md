# AGM Store Builder - Python FastAPI Backend File Structure

> Complete file structure for Python FastAPI backend (HuggingFace Spaces compatible)

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Complete Directory Structure](#complete-directory-structure)
3. [Technology Stack](#technology-stack)
4. [Dependencies (requirements.txt)](#dependencies-requirementstxt)
5. [UV Installation Commands](#uv-installation-commands)
6. [File Descriptions](#file-descriptions)
7. [Database Schema (MySQL)](#database-schema-mysql)
8. [Environment Variables](#environment-variables)
9. [HuggingFace Deployment](#huggingface-deployment)

---

## Project Overview

This is a Python FastAPI backend for the AGM Store Builder e-commerce platform, designed for:
- **HuggingFace Spaces deployment**
- **MySQL database** (same schema as Node.js version)
- **Monnify payment integration** (Nigerian payment gateway)
- **JWT authentication**
- **File uploads** (Cloudinary)
- **Email/SMS notifications** (SendGrid/Termii)

---

## 📁 Complete Directory Structure

```
agm-store-builder-backend-python/
│
├── 📄 pyproject.toml                    # UV/pip project config
├── 📄 requirements.txt                   # Python dependencies
├── 📄 .env.example                       # Environment template
├── 📄 .gitignore                         # Git ignore
├── 📄 README.md                          # Documentation
├── 📄 Dockerfile                         # Docker config
├── 📄 docker-compose.yml                 # Docker compose
│
├── 📁 app/                               # Main application
│   │
│   ├── 📄 __init__.py                    # Package init
│   ├── 📄 main.py                        # FastAPI entry point (CRITICAL)
│   ├── 📄 config.py                      # Configuration settings
│   ├── 📄 dependencies.py                # Dependency injection
│   │
│   ├── 📁 core/                          # Core modules
│   │   ├── 📄 __init__.py
│   │   ├── 📄 config.py                  # Settings & environment
│   │   ├── 📄 security.py                # JWT & password hashing
│   │   ├── 📄 exceptions.py              # Custom exceptions
│   │   └── 📄 constants.py               # App constants
│   │
│   ├── 📁 database/                      # Database layer
│   │   ├── 📄 __init__.py
│   │   ├── 📄 connection.py              # MySQL connection pool (CRITICAL)
│   │   ├── 📄 session.py                 # Database session management
│   │   └── 📄 base.py                    # SQLAlchemy base
│   │
│   ├── 📁 models/                        # SQLAlchemy ORM models
│   │   ├── 📄 __init__.py                # Model exports
│   │   ├── 📄 user.py                    # User model
│   │   ├── 📄 user_settings.py           # User settings model
│   │   ├── 📄 store.py                   # Store model
│   │   ├── 📄 product.py                 # Product model
│   │   ├── 📄 order.py                   # Order model
│   │   ├── 📄 order_item.py              # Order item model
│   │   ├── 📄 payment.py                 # Payment model
│   │   ├── 📄 bank_account.py            # Bank account model
│   │   ├── 📄 otp_verification.py        # OTP verification model
│   │   └── 📄 refresh_token.py           # Refresh token model
│   │
│   ├── 📁 schemas/                       # Pydantic schemas
│   │   ├── 📄 __init__.py
│   │   ├── 📄 auth.py                    # Auth request/response schemas
│   │   ├── 📄 user.py                    # User schemas
│   │   ├── 📄 store.py                   # Store schemas
│   │   ├── 📄 product.py                 # Product schemas
│   │   ├── 📄 order.py                   # Order schemas
│   │   ├── 📄 payment.py                 # Payment schemas
│   │   ├── 📄 bank_account.py            # Bank account schemas
│   │   ├── 📄 analytics.py               # Analytics schemas
│   │   └── 📄 common.py                  # Shared schemas (response, pagination)
│   │
│   ├── 📁 api/                           # API routes
│   │   ├── 📄 __init__.py
│   │   │
│   │   ├── 📁 v1/                        # API version 1
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 router.py              # V1 router aggregator (CRITICAL)
│   │   │   ├── 📄 auth.py                # /api/v1/auth/*
│   │   │   ├── 📄 users.py               # /api/v1/users/*
│   │   │   ├── 📄 stores.py              # /api/v1/stores/*
│   │   │   ├── 📄 products.py            # /api/v1/products/*
│   │   │   ├── 📄 orders.py              # /api/v1/orders/*
│   │   │   ├── 📄 payments.py            # /api/v1/payments/*
│   │   │   ├── 📄 analytics.py           # /api/v1/analytics/*
│   │   │   ├── 📄 upload.py              # /api/v1/upload/*
│   │   │   ├── 📄 webhooks.py            # /api/v1/webhooks/*
│   │   │   └── 📄 health.py              # /api/v1/health
│   │   │
│   │   └── 📄 deps.py                    # API dependencies (auth, db)
│   │
│   ├── 📁 services/                      # Business logic layer
│   │   ├── 📄 __init__.py
│   │   ├── 📄 auth_service.py            # Authentication logic
│   │   ├── 📄 user_service.py            # User operations
│   │   ├── 📄 store_service.py           # Store operations
│   │   ├── 📄 product_service.py         # Product operations
│   │   ├── 📄 order_service.py           # Order operations
│   │   ├── 📄 payment_service.py         # Payment logic
│   │   ├── 📄 monnify_service.py         # Monnify API integration (CRITICAL)
│   │   ├── 📄 email_service.py           # Email sending (SendGrid)
│   │   ├── 📄 sms_service.py             # SMS sending (Termii)
│   │   ├── 📄 upload_service.py          # File upload (Cloudinary)
│   │   ├── 📄 otp_service.py             # OTP generation/verification
│   │   └── 📄 analytics_service.py       # Analytics calculations
│   │
│   ├── 📁 repositories/                  # Data access layer (optional pattern)
│   │   ├── 📄 __init__.py
│   │   ├── 📄 base.py                    # Base repository
│   │   ├── 📄 user_repository.py         # User data operations
│   │   ├── 📄 store_repository.py        # Store data operations
│   │   ├── 📄 product_repository.py      # Product data operations
│   │   ├── 📄 order_repository.py        # Order data operations
│   │   └── 📄 payment_repository.py      # Payment data operations
│   │
│   ├── 📁 middleware/                    # FastAPI middleware
│   │   ├── 📄 __init__.py
│   │   ├── 📄 cors.py                    # CORS configuration
│   │   ├── 📄 rate_limit.py              # Rate limiting
│   │   ├── 📄 logging.py                 # Request logging
│   │   └── 📄 error_handler.py           # Global error handler (CRITICAL)
│   │
│   ├── 📁 utils/                         # Utility functions
│   │   ├── 📄 __init__.py
│   │   ├── 📄 jwt.py                     # JWT operations
│   │   ├── 📄 password.py                # Password hashing (bcrypt)
│   │   ├── 📄 otp.py                     # OTP generation
│   │   ├── 📄 slugify.py                 # Slug generation
│   │   ├── 📄 validators.py              # Custom validators
│   │   ├── 📄 helpers.py                 # General helpers
│   │   ├── 📄 constants.py               # Constants
│   │   └── 📄 response.py                # Response formatter
│   │
│   └── 📁 templates/                     # Email/SMS templates
│       ├── 📄 __init__.py
│       ├── 📁 email/
│       │   ├── welcome.html              # Welcome email
│       │   ├── otp.html                  # OTP email
│       │   ├── order_confirmation.html   # Order confirmation
│       │   ├── payment_received.html     # Payment received
│       │   └── payout_completed.html     # Payout completed
│       │
│       └── 📁 sms/
│           ├── otp.py                    # OTP SMS template
│           ├── order_confirmed.py        # Order confirmed
│           └── payment_received.py       # Payment received
│
├── 📁 migrations/                        # Alembic migrations (optional)
│   ├── 📄 env.py
│   ├── 📄 script.py.mako
│   └── 📁 versions/
│       └── 📄 001_initial.py
│
├── 📁 tests/                             # Test files
│   ├── 📄 __init__.py
│   ├── 📄 conftest.py                    # Pytest fixtures
│   │
│   ├── 📁 unit/
│   │   ├── 📄 test_auth_service.py
│   │   ├── 📄 test_user_service.py
│   │   └── 📄 test_utils.py
│   │
│   └── 📁 integration/
│       ├── 📄 test_auth_api.py
│       ├── 📄 test_stores_api.py
│       ├── 📄 test_products_api.py
│       └── 📄 test_orders_api.py
│
└── 📁 scripts/                           # Utility scripts
    ├── 📄 create_admin.py                # Create admin user
    ├── 📄 seed_data.py                   # Seed test data
    └── 📄 cleanup_expired.py             # Cleanup expired tokens/OTPs
```

---

## 📊 File Count Summary

| Directory | File Count |
|-----------|------------|
| Root | 7 files |
| app/core | 5 files |
| app/database | 4 files |
| app/models | 11 files |
| app/schemas | 10 files |
| app/api/v1 | 12 files |
| app/services | 13 files |
| app/repositories | 7 files |
| app/middleware | 5 files |
| app/utils | 9 files |
| app/templates | 9 files |
| migrations | 3 files |
| tests | 8 files |
| scripts | 3 files |
| **Total** | **~106 files** |

---

## 🎯 Technology Stack

**Core:**
- Python 3.11+
- FastAPI 0.104+
- Uvicorn (ASGI server)

**Database:**
- MySQL 8.0
- SQLAlchemy 2.0 (ORM)
- aiomysql (async MySQL driver)

**Authentication:**
- python-jose (JWT)
- passlib[bcrypt] (password hashing)

**Validation:**
- Pydantic v2

**Payments:**
- Monnify API
- httpx (async HTTP client)

**File Upload:**
- Cloudinary
- python-multipart

**Communication:**
- SendGrid (email)
- Termii API (SMS)

**Security:**
- python-multipart
- slowapi (rate limiting)

**Development:**
- pytest
- pytest-asyncio
- httpx (testing)
- black (formatting)
- ruff (linting)

---

## 📦 Dependencies (requirements.txt)

```txt
# =============================================================================
# AGM Store Builder - Python FastAPI Backend Dependencies
# =============================================================================

# Core Framework
fastapi==0.109.2
uvicorn[standard]==0.27.1
python-multipart==0.0.9
pydantic==2.6.1
pydantic-settings==2.2.1

# Database
sqlalchemy==2.0.27
aiomysql==0.2.0
pymysql==1.1.0
alembic==1.13.1

# Authentication & Security
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
bcrypt==4.1.2

# HTTP Client (for external APIs)
httpx==0.26.0
aiohttp==3.9.3

# File Upload
cloudinary==1.38.0
python-magic==0.4.27

# Email
sendgrid==6.11.0

# SMS (Termii uses httpx)
# No additional package needed

# Utilities
python-dotenv==1.0.1
python-dateutil==2.8.2
email-validator==2.1.0.post1
slowapi==0.1.9

# Logging & Monitoring
loguru==0.7.2

# Development
pytest==8.0.0
pytest-asyncio==0.23.4
pytest-cov==4.1.0
httpx==0.26.0
black==24.2.0
ruff==0.2.1
mypy==1.8.0
pre-commit==3.6.0

# Production
gunicorn==21.2.0
```

---

## 🚀 UV Installation Commands

```bash
# Initialize project with uv
uv init .

# Add core dependencies
uv add fastapi uvicorn[standard] python-multipart pydantic pydantic-settings

# Add database dependencies
uv add sqlalchemy aiomysql pymysql alembic

# Add authentication dependencies
uv add python-jose[cryptography] passlib[bcrypt] bcrypt

# Add HTTP client
uv add httpx aiohttp

# Add file upload
uv add cloudinary python-magic

# Add email
uv add sendgrid

# Add utilities
uv add python-dotenv python-dateutil email-validator slowapi loguru

# Add development dependencies
uv add --dev pytest pytest-asyncio pytest-cov black ruff mypy pre-commit

# Add production server
uv add gunicorn

# Or install all at once:
uv add fastapi uvicorn[standard] python-multipart pydantic pydantic-settings sqlalchemy aiomysql pymysql alembic python-jose[cryptography] passlib[bcrypt] bcrypt httpx aiohttp cloudinary python-magic sendgrid python-dotenv python-dateutil email-validator slowapi loguru gunicorn

uv add --dev pytest pytest-asyncio pytest-cov black ruff mypy pre-commit
```

---

## 📁 File Descriptions

### Critical Files (Build First)

#### Phase 1: Foundation (5 files)
1. **`app/main.py`** - FastAPI app entry point with lifespan events
2. **`app/core/config.py`** - Settings class with environment variables
3. **`app/database/connection.py`** - MySQL async connection pool
4. **`app/middleware/error_handler.py`** - Global exception handler
5. **`app/api/v1/router.py`** - API router aggregator

#### Phase 2: Database (12 files)
6. **`app/database/base.py`** - SQLAlchemy declarative base
7. **`app/database/session.py`** - Database session factory
8. **`app/models/*.py`** - All 10 SQLAlchemy models

#### Phase 3: Authentication (8 files)
9. **`app/schemas/auth.py`** - Auth Pydantic schemas
10. **`app/services/auth_service.py`** - Auth business logic
11. **`app/api/v1/auth.py`** - Auth API endpoints
12. **`app/utils/jwt.py`** - JWT utilities
13. **`app/utils/password.py`** - Password hashing
14. **`app/api/deps.py`** - Authentication dependencies

#### Phase 4: Core Features
15-40. Models, schemas, services, routes for stores, products, orders

#### Phase 5: Payments (Monnify)
41. **`app/services/monnify_service.py`** - Monnify API integration
42. **`app/api/v1/payments.py`** - Payment endpoints
43. **`app/api/v1/webhooks.py`** - Webhook handlers

#### Phase 6: Supporting Services
44-100+. Upload, email, SMS, analytics, etc.

---

## 🗄️ Database Schema (MySQL)

```sql
-- =============================================================================
-- AGM Store Builder - Complete MySQL Database Schema
-- =============================================================================
-- Database: agm_store_builder
-- Engine: MySQL 8.0+
-- Character Set: utf8mb4
-- Collation: utf8mb4_unicode_ci
-- =============================================================================

-- TABLE 1: users
CREATE TABLE IF NOT EXISTS users (
    id CHAR(36) PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    phone VARCHAR(20) UNIQUE,
    avatar_url VARCHAR(500) DEFAULT NULL,
    role ENUM('user', 'admin', 'super_admin') DEFAULT 'user',
    email_verified BOOLEAN DEFAULT FALSE,
    phone_verified BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    has_completed_onboarding BOOLEAN DEFAULT FALSE,
    last_login_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    
    INDEX idx_email (email),
    INDEX idx_phone (phone),
    INDEX idx_role (role),
    INDEX idx_active (is_active),
    INDEX idx_email_verified (email_verified),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- TABLE 2: user_settings
CREATE TABLE IF NOT EXISTS user_settings (
    id CHAR(36) PRIMARY KEY,
    user_id CHAR(36) NOT NULL UNIQUE,
    email_notifications BOOLEAN DEFAULT TRUE,
    sms_notifications BOOLEAN DEFAULT TRUE,
    order_notifications BOOLEAN DEFAULT TRUE,
    payment_notifications BOOLEAN DEFAULT TRUE,
    payout_notifications BOOLEAN DEFAULT TRUE,
    marketing_notifications BOOLEAN DEFAULT FALSE,
    profile_visibility ENUM('public', 'private') DEFAULT 'public',
    show_email BOOLEAN DEFAULT FALSE,
    show_phone BOOLEAN DEFAULT FALSE,
    default_currency VARCHAR(3) DEFAULT 'NGN',
    timezone VARCHAR(50) DEFAULT 'Africa/Lagos',
    language VARCHAR(10) DEFAULT 'en',
    two_factor_enabled BOOLEAN DEFAULT FALSE,
    login_alerts BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- TABLE 3: stores
CREATE TABLE IF NOT EXISTS stores (
    id CHAR(36) PRIMARY KEY,
    user_id CHAR(36) NOT NULL,
    username VARCHAR(100) NOT NULL UNIQUE,
    display_name VARCHAR(255) NOT NULL,
    description TEXT,
    logo_url VARCHAR(500),
    banner_url VARCHAR(500),
    template_id ENUM('products', 'bookings', 'portfolio') DEFAULT 'products',
    category VARCHAR(100),
    custom_colors JSON,
    custom_fonts JSON,
    social_links JSON,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_username (username),
    INDEX idx_category (category),
    INDEX idx_template_id (template_id),
    INDEX idx_active (is_active),
    INDEX idx_created_at (created_at),
    FULLTEXT idx_search (display_name, description)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- TABLE 4: products
CREATE TABLE IF NOT EXISTS products (
    id CHAR(36) PRIMARY KEY,
    store_id CHAR(36) NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(12, 2) NOT NULL,
    compare_at_price DECIMAL(12, 2),
    cost_price DECIMAL(12, 2),
    sku VARCHAR(100),
    barcode VARCHAR(100),
    stock_quantity INT DEFAULT 0,
    low_stock_threshold INT DEFAULT 5,
    weight DECIMAL(10, 2),
    dimensions JSON,
    images JSON NOT NULL DEFAULT '[]',
    variations JSON,
    category VARCHAR(100),
    tags JSON,
    is_active BOOLEAN DEFAULT TRUE,
    is_featured BOOLEAN DEFAULT FALSE,
    view_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    
    FOREIGN KEY (store_id) REFERENCES stores(id) ON DELETE CASCADE,
    INDEX idx_store_id (store_id),
    INDEX idx_category (category),
    INDEX idx_price (price),
    INDEX idx_sku (sku),
    INDEX idx_active (is_active),
    INDEX idx_featured (is_featured),
    INDEX idx_stock (stock_quantity),
    INDEX idx_created_at (created_at),
    FULLTEXT idx_search (name, description)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- TABLE 5: orders
CREATE TABLE IF NOT EXISTS orders (
    id CHAR(36) PRIMARY KEY,
    store_id CHAR(36) NOT NULL,
    order_number VARCHAR(50) NOT NULL UNIQUE,
    customer_name VARCHAR(255) NOT NULL,
    customer_email VARCHAR(255),
    customer_phone VARCHAR(20) NOT NULL,
    customer_address JSON,
    delivery_address TEXT,
    delivery_state VARCHAR(100),
    delivery_lga VARCHAR(100),
    items JSON NOT NULL,
    subtotal DECIMAL(12, 2) NOT NULL,
    discount DECIMAL(12, 2) DEFAULT 0,
    shipping_fee DECIMAL(12, 2) DEFAULT 0,
    agm_fee DECIMAL(12, 2) NOT NULL DEFAULT 0,
    total DECIMAL(12, 2) NOT NULL,
    status ENUM('pending', 'confirmed', 'processing', 'shipped', 'delivered', 'fulfilled', 'cancelled') DEFAULT 'pending',
    payment_status ENUM('pending', 'paid', 'failed', 'expired', 'refunded') DEFAULT 'pending',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    
    FOREIGN KEY (store_id) REFERENCES stores(id) ON DELETE CASCADE,
    INDEX idx_store_id (store_id),
    INDEX idx_order_number (order_number),
    INDEX idx_customer_email (customer_email),
    INDEX idx_customer_phone (customer_phone),
    INDEX idx_status (status),
    INDEX idx_payment_status (payment_status),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- TABLE 6: order_items
CREATE TABLE IF NOT EXISTS order_items (
    id CHAR(36) PRIMARY KEY,
    order_id CHAR(36) NOT NULL,
    product_id CHAR(36) NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    product_image VARCHAR(500),
    product_price DECIMAL(12, 2) NOT NULL,
    quantity INT NOT NULL,
    subtotal DECIMAL(12, 2) NOT NULL,
    variant_selection JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE RESTRICT,
    INDEX idx_order_id (order_id),
    INDEX idx_product_id (product_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- TABLE 7: payments
CREATE TABLE IF NOT EXISTS payments (
    id CHAR(36) PRIMARY KEY,
    order_id CHAR(36) NOT NULL,
    user_id CHAR(36) NOT NULL,
    amount DECIMAL(12, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'NGN',
    status ENUM('pending', 'paid', 'failed', 'expired', 'refunded') DEFAULT 'pending',
    payment_method ENUM('bank_transfer', 'card', 'ussd') DEFAULT NULL,
    payment_reference VARCHAR(100) NOT NULL UNIQUE,
    monnify_reference VARCHAR(100) UNIQUE,
    account_number VARCHAR(20),
    account_name VARCHAR(255),
    bank_name VARCHAR(100),
    metadata JSON,
    paid_at TIMESTAMP NULL,
    expires_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_order_id (order_id),
    INDEX idx_user_id (user_id),
    INDEX idx_payment_reference (payment_reference),
    INDEX idx_monnify_reference (monnify_reference),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- TABLE 8: bank_accounts
CREATE TABLE IF NOT EXISTS bank_accounts (
    id CHAR(36) PRIMARY KEY,
    user_id CHAR(36) NOT NULL,
    account_number VARCHAR(20) NOT NULL,
    account_name VARCHAR(255) NOT NULL,
    bank_code VARCHAR(10) NOT NULL,
    bank_name VARCHAR(255) NOT NULL,
    is_verified BOOLEAN DEFAULT FALSE,
    is_primary BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_account_number (account_number),
    INDEX idx_bank_code (bank_code),
    UNIQUE KEY unique_account (user_id, account_number, bank_code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- TABLE 9: otp_verifications
CREATE TABLE IF NOT EXISTS otp_verifications (
    id CHAR(36) PRIMARY KEY,
    email VARCHAR(255),
    phone VARCHAR(20),
    code VARCHAR(6) NOT NULL,
    type ENUM('email', 'phone', 'password_reset', 'login') NOT NULL,
    verified BOOLEAN DEFAULT FALSE,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_email (email),
    INDEX idx_phone (phone),
    INDEX idx_code (code),
    INDEX idx_type (type),
    INDEX idx_verified (verified),
    INDEX idx_expires_at (expires_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- TABLE 10: refresh_tokens
CREATE TABLE IF NOT EXISTS refresh_tokens (
    id CHAR(36) PRIMARY KEY,
    user_id CHAR(36) NOT NULL,
    token_hash VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    revoked BOOLEAN DEFAULT FALSE,
    revoked_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_token_hash (token_hash),
    INDEX idx_expires_at (expires_at),
    INDEX idx_revoked (revoked)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

---

## 🔐 Environment Variables

```env
# =============================================================================
# AGM Store Builder - Python FastAPI Environment Variables
# =============================================================================

# Application
APP_ENV=development
APP_DEBUG=true
APP_NAME="AGM Store Builder"
APP_URL=http://localhost:8000
FRONTEND_URL=http://localhost:3000

# Server
HOST=0.0.0.0
PORT=8000

# Database (MySQL)
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=agm_store_builder

# JWT Authentication
JWT_SECRET_KEY=your-super-secret-key-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# Monnify Payment Gateway
MONNIFY_BASE_URL=https://sandbox.monnify.com
MONNIFY_API_KEY=your_monnify_api_key
MONNIFY_SECRET_KEY=your_monnify_secret_key
MONNIFY_CONTRACT_CODE=your_monnify_contract_code
MONNIFY_WEBHOOK_SECRET=your_monnify_webhook_secret

# Cloudinary (Image Storage)
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_cloudinary_api_key
CLOUDINARY_API_SECRET=your_cloudinary_api_secret

# SendGrid (Email)
SENDGRID_API_KEY=your_sendgrid_api_key
SENDGRID_FROM_EMAIL=noreply@agmshops.com
SENDGRID_FROM_NAME="AGM Store Builder"

# Termii (SMS)
TERMII_API_KEY=your_termii_api_key
TERMII_SENDER_ID="AGM Store"

# AGM Configuration
AGM_FEE_PERCENTAGE=2.5

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60

# CORS
CORS_ORIGINS=["http://localhost:3000", "https://agmshops.com"]

# Logging
LOG_LEVEL=INFO
```

---

## 🤗 HuggingFace Deployment

### HuggingFace Spaces Configuration

Create a `Dockerfile` for HuggingFace Spaces:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libmariadb-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 7860

# Run with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
```

### HuggingFace Space README (README.md)

```yaml
---
title: AGM Store Builder API
emoji: 🛍️
colorFrom: purple
colorTo: blue
sdk: docker
pinned: false
license: mit
---

# AGM Store Builder API

FastAPI backend for the AGM Store Builder e-commerce platform.

## API Documentation

Visit `/docs` for Swagger UI or `/redoc` for ReDoc documentation.
```

---

## 🚀 Quick Start Commands

```bash
# 1. Initialize project with uv
uv init .

# 2. Install all dependencies
uv sync

# 3. Set up environment
cp .env.example .env
# Edit .env with your values

# 4. Run database migrations (if using Alembic)
alembic upgrade head

# 5. Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 6. Run tests
pytest

# 7. Format code
black app/
ruff check app/ --fix

# 8. Production start
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

---

## 📝 API Endpoints Overview

| Endpoint | Methods | Description |
|----------|---------|-------------|
| `/api/v1/auth/register` | POST | User registration |
| `/api/v1/auth/login` | POST | User login |
| `/api/v1/auth/verify-otp` | POST | Verify OTP |
| `/api/v1/auth/refresh` | POST | Refresh token |
| `/api/v1/auth/logout` | POST | Logout |
| `/api/v1/auth/forgot-password` | POST | Request password reset |
| `/api/v1/auth/reset-password` | POST | Reset password |
| `/api/v1/users/me` | GET, PUT | User profile |
| `/api/v1/users/change-password` | POST | Change password |
| `/api/v1/stores` | GET, POST | Store CRUD |
| `/api/v1/stores/{username}` | GET | Public store |
| `/api/v1/stores/check/{username}` | GET | Check availability |
| `/api/v1/stores/my-stores` | GET | User's stores |
| `/api/v1/products` | GET, POST | Products CRUD |
| `/api/v1/products/my-products` | GET | User's products |
| `/api/v1/orders` | GET, POST | Orders CRUD |
| `/api/v1/orders/track/{orderNumber}` | GET | Track order |
| `/api/v1/payments/verify/{reference}` | GET | Verify payment |
| `/api/v1/payments/bank-accounts` | GET, POST | Bank accounts |
| `/api/v1/analytics/dashboard` | GET | Dashboard stats |
| `/api/v1/upload/image` | POST | Upload image |
| `/api/v1/webhooks/monnify` | POST | Monnify webhook |
| `/api/v1/health` | GET | Health check |

---

**Last Updated**: January 20, 2026  
**Maintained By**: @thetruesammyjay
