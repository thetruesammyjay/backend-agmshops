"""
Tests for app.core.security — JWT tokens and password hashing.
"""

from datetime import timedelta

import pytest

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    create_tokens,
    decode_token,
    verify_access_token,
    verify_refresh_token,
    create_password_reset_token,
    verify_password_reset_token,
)
from app.core.exceptions import TokenError


# ── Password Hashing ──────────────────────────────────────────────


class TestPasswordHashing:
    def test_hash_password_returns_bcrypt_hash(self):
        hashed = hash_password("MyPassword1")
        assert hashed.startswith("$2b$") or hashed.startswith("$2a$")

    def test_verify_password_correct(self):
        hashed = hash_password("SecurePass1")
        assert verify_password("SecurePass1", hashed) is True

    def test_verify_password_wrong(self):
        hashed = hash_password("SecurePass1")
        assert verify_password("WrongPassword1", hashed) is False

    def test_verify_password_garbage_hash(self):
        assert verify_password("anything", "not-a-hash") is False

    def test_different_passwords_produce_different_hashes(self):
        h1 = hash_password("Password1")
        h2 = hash_password("Password2")
        assert h1 != h2


# ── Access Tokens ─────────────────────────────────────────────────


class TestAccessTokens:
    def test_create_and_verify_access_token(self):
        token = create_access_token(data={"sub": "user-123"})
        user_id = verify_access_token(token)
        assert user_id == "user-123"

    def test_access_token_custom_expiry(self):
        token = create_access_token(
            data={"sub": "user-456"},
            expires_delta=timedelta(minutes=5),
        )
        user_id = verify_access_token(token)
        assert user_id == "user-456"

    def test_verify_access_token_rejects_refresh_token(self):
        token = create_refresh_token(data={"sub": "user-789"})
        with pytest.raises(TokenError):
            verify_access_token(token)

    def test_verify_access_token_rejects_garbage(self):
        with pytest.raises(TokenError):
            verify_access_token("not.a.real.token")

    def test_expired_access_token_raises(self):
        token = create_access_token(
            data={"sub": "user-expired"},
            expires_delta=timedelta(seconds=-1),
        )
        with pytest.raises(TokenError):
            verify_access_token(token)


# ── Refresh Tokens ────────────────────────────────────────────────


class TestRefreshTokens:
    def test_create_and_verify_refresh_token(self):
        token = create_refresh_token(data={"sub": "user-100"})
        user_id = verify_refresh_token(token)
        assert user_id == "user-100"

    def test_refresh_token_custom_expiry(self):
        token = create_refresh_token(
            data={"sub": "user-200"},
            expires_delta=timedelta(days=1),
        )
        user_id = verify_refresh_token(token)
        assert user_id == "user-200"

    def test_verify_refresh_token_rejects_access_token(self):
        token = create_access_token(data={"sub": "user-300"})
        with pytest.raises(TokenError):
            verify_refresh_token(token)


# ── Token Pairs ───────────────────────────────────────────────────


class TestCreateTokens:
    def test_create_tokens_returns_both(self):
        tokens = create_tokens("user-pair")
        assert "accessToken" in tokens
        assert "refreshToken" in tokens
        assert verify_access_token(tokens["accessToken"]) == "user-pair"
        assert verify_refresh_token(tokens["refreshToken"]) == "user-pair"


# ── Decode Token ──────────────────────────────────────────────────


class TestDecodeToken:
    def test_decode_valid_token(self):
        token = create_access_token(data={"sub": "user-decode"})
        payload = decode_token(token)
        assert payload["sub"] == "user-decode"
        assert payload["token_type"] == "access"

    def test_decode_invalid_token_raises(self):
        with pytest.raises(TokenError):
            decode_token("invalid-token")


# ── Password Reset Tokens ────────────────────────────────────────


class TestPasswordResetTokens:
    def test_create_and_verify_reset_token(self):
        token = create_password_reset_token("user-reset")
        user_id = verify_password_reset_token(token)
        assert user_id == "user-reset"

    def test_reset_token_rejected_as_access_token(self):
        token = create_password_reset_token("user-reset")
        with pytest.raises(TokenError):
            verify_access_token(token)

    def test_access_token_rejected_as_reset_token(self):
        token = create_access_token(data={"sub": "user-fake"})
        with pytest.raises(TokenError):
            verify_password_reset_token(token)
