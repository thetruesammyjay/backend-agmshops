# Backend API Endpoints

Base URL: `http://localhost:8000/api/v1` (unless otherwise noted)

## Authentication (`/auth`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/register` | Register a new user account | No |
| POST | `/signup` | Signup (alias for register) | No |
| POST | `/login` | Login with email and password | No |
| POST | `/refresh` | Get new access token using refresh token | No |
| POST | `/logout` | Logout the current user | Yes |
| POST | `/forgot-password` | Request a password reset OTP | No |
| POST | `/verify-otp` | Verify an OTP code | No |
| POST | `/reset-password` | Reset password using verified reset token | No |
| POST | `/resend-verification` | Resend email verification OTP | No |

## Users (`/users`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/me` | Get the authenticated user's profile | Yes |
| PUT | `/me` | Update the authenticated user's profile | Yes |
| POST | `/change-password` | Change the authenticated user's password | Yes |
| DELETE | `/me` | Delete the authenticated user's account | Yes |

## Stores (`/stores`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/` | Create a new store | Yes |
| GET | `/check/{username}` | Check if a store username is available | No |
| GET | `/my-stores` | Get all stores owned by the authenticated user | Yes |
| GET | `/{username}` | Get public store details by username | No |
| GET | `/id/{store_id}` | Get store details by ID (owner only) | Yes |
| PUT | `/{store_id}` | Update store details (owner only) | Yes |
| PATCH | `/{store_id}/status` | Activate or deactivate a store | Yes |
| DELETE | `/{store_id}` | Delete a store (soft delete) | Yes |

## Products (`/products`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/` | Create a new product | Yes |
| GET | `/my-products` | Get all products for the authenticated user's stores | Yes |
| GET | `/{product_id}` | Get product details by ID (owner only) | Yes |
| PUT | `/{product_id}` | Update product details (owner only) | Yes |
| PATCH | `/{product_id}/stock` | Update product stock quantity | Yes |
| PATCH | `/{product_id}/status` | Activate or deactivate a product | Yes |
| PATCH | `/bulk-update` | Update multiple products at once | Yes |
| DELETE | `/{product_id}` | Delete a product (soft delete) | Yes |

## Orders (`/orders`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/` | Create a new order (public checkout) | No |
| GET | `/track/{order_number}` | Track an order by order number | No |
| GET | `/` | Get all orders for the user's stores | Yes |
| GET | `/{order_id}` | Get order details by ID (owner only) | Yes |
| PATCH | `/{order_id}/status` | Update order status (owner only) | Yes |
| DELETE | `/{order_id}` | Cancel an order (owner only) | Yes |

## Payments (`/payments`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/verify/{reference}` | Verify payment status by reference | No |
| GET | `/{reference}` | Get payment details by reference | No |
| POST | `/{reference}/reinitialize` | Reinitialize an expired payment | No |
| POST | `/bank-accounts` | Add a bank account for payouts | Yes |
| GET | `/bank-accounts` | Get user's bank accounts | Yes |
| PUT | `/bank-accounts/{account_id}/primary` | Set a bank account as primary | Yes |
| DELETE | `/bank-accounts/{account_id}` | Delete a bank account | Yes |
| GET | `/banks` | Get list of Nigerian banks | No |

## Analytics (`/analytics`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/dashboard` | Get dashboard analytics overview | Yes |
| GET | `/revenue` | Get revenue statistics | Yes |
| GET | `/orders` | Get order statistics | Yes |
| GET | `/products` | Get product performance analytics | Yes |
| GET | `/customers` | Get customer analytics | Yes |

## Upload (`/upload`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/image` | Upload a single image to Cloudinary | Yes |
| POST | `/images` | Upload multiple images to Cloudinary | Yes |
| DELETE | `/image/{public_id:path}` | Delete an image from Cloudinary | Yes |

## Webhooks (`/webhooks`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/monnify` | Handle Monnify payment webhooks | No |

## System / Health

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/` | Root endpoint (Health check) | No |
| GET | `/health` | Health check endpoint | No |
| GET | `/api/v1/health` | API Version Health check | No |
| GET | `/api/v1/version` | API Version Info | No |
