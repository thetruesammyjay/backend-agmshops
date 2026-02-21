"""
Tests for app.schemas.auth — Pydantic schema validation.
"""

import pytest
from pydantic import ValidationError

from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    RefreshTokenRequest,
    VerifyOTPRequest,
    ResetPasswordRequest,
    ResendVerificationRequest,
)


# ── RegisterRequest ───────────────────────────────────────────────


class TestRegisterRequest:
    def test_valid_registration(self):
        req = RegisterRequest(
            email="user@example.com",
            password="SecurePass1",
            full_name="John Doe",
        )
        assert req.email == "user@example.com"
        assert req.full_name == "John Doe"

    def test_with_phone(self):
        req = RegisterRequest(
            email="user@example.com",
            password="SecurePass1",
            full_name="John Doe",
            phone="08012345678",
        )
        assert req.phone == "08012345678"

    def test_invalid_email_raises(self):
        with pytest.raises(ValidationError):
            RegisterRequest(
                email="not-an-email",
                password="SecurePass1",
                full_name="John Doe",
            )

    def test_password_too_short_raises(self):
        with pytest.raises(ValidationError):
            RegisterRequest(
                email="user@example.com",
                password="Short1",
                full_name="John Doe",
            )

    def test_password_no_uppercase_raises(self):
        with pytest.raises(ValidationError):
            RegisterRequest(
                email="user@example.com",
                password="alllowercase1",
                full_name="John Doe",
            )

    def test_password_no_lowercase_raises(self):
        with pytest.raises(ValidationError):
            RegisterRequest(
                email="user@example.com",
                password="ALLUPPERCASE1",
                full_name="John Doe",
            )

    def test_password_no_digit_raises(self):
        with pytest.raises(ValidationError):
            RegisterRequest(
                email="user@example.com",
                password="NoDigitsHere",
                full_name="John Doe",
            )

    def test_full_name_too_short_raises(self):
        with pytest.raises(ValidationError):
            RegisterRequest(
                email="user@example.com",
                password="SecurePass1",
                full_name="J",
            )


# ── LoginRequest ──────────────────────────────────────────────────


class TestLoginRequest:
    def test_valid_login(self):
        req = LoginRequest(
            email="user@example.com",
            password="mypassword",
        )
        assert req.email == "user@example.com"

    def test_invalid_email_raises(self):
        with pytest.raises(ValidationError):
            LoginRequest(email="bad-email", password="pass")


# ── RefreshTokenRequest ───────────────────────────────────────────


class TestRefreshTokenRequest:
    def test_valid_request(self):
        req = RefreshTokenRequest(refreshToken="some-token-string")
        assert req.refreshToken == "some-token-string"


# ── VerifyOTPRequest ──────────────────────────────────────────────


class TestVerifyOTPRequest:
    def test_valid_otp(self):
        req = VerifyOTPRequest(
            email="user@example.com",
            otp="123456",
        )
        assert req.otp == "123456"
        assert req.type == "email"  # default

    def test_otp_too_short_raises(self):
        with pytest.raises(ValidationError):
            VerifyOTPRequest(
                email="user@example.com",
                otp="123",
            )

    def test_otp_too_long_raises(self):
        with pytest.raises(ValidationError):
            VerifyOTPRequest(
                email="user@example.com",
                otp="1234567",
            )

    def test_custom_type(self):
        req = VerifyOTPRequest(
            email="user@example.com",
            otp="123456",
            type="password_reset",
        )
        assert req.type == "password_reset"


# ── ResetPasswordRequest ─────────────────────────────────────────


class TestResetPasswordRequest:
    def test_valid_request(self):
        req = ResetPasswordRequest(
            resetToken="reset-token-123",
            newPassword="NewSecure1",
        )
        assert req.resetToken == "reset-token-123"

    def test_weak_password_raises(self):
        with pytest.raises(ValidationError):
            ResetPasswordRequest(
                resetToken="token",
                newPassword="weak",
            )

    def test_no_uppercase_raises(self):
        with pytest.raises(ValidationError):
            ResetPasswordRequest(
                resetToken="token",
                newPassword="alllowercase1",
            )


# ── ResendVerificationRequest ────────────────────────────────────


class TestResendVerificationRequest:
    def test_valid_request(self):
        req = ResendVerificationRequest(email="user@example.com")
        assert req.email == "user@example.com"

    def test_invalid_email_raises(self):
        with pytest.raises(ValidationError):
            ResendVerificationRequest(email="bad")
