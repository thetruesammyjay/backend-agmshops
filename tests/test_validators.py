"""
Tests for app.utils.validators — input validation functions.
"""

import pytest

from app.utils.validators import (
    ValidationError,
    validate_email,
    validate_password,
    validate_phone,
    validate_username,
    validate_account_number,
    validate_price,
    validate_quantity,
    validate_image_url,
)


# ── Email Validation ─────────────────────────────────────────────


class TestValidateEmail:
    def test_valid_email(self):
        assert validate_email("user@example.com") is True

    def test_valid_email_with_dots(self):
        assert validate_email("first.last@domain.co.uk") is True

    def test_empty_email_raises(self):
        with pytest.raises(ValidationError, match="required"):
            validate_email("")

    def test_invalid_format_raises(self):
        with pytest.raises(ValidationError, match="Invalid email"):
            validate_email("not-an-email")

    def test_missing_domain_raises(self):
        with pytest.raises(ValidationError, match="Invalid email"):
            validate_email("user@")


# ── Password Validation ──────────────────────────────────────────


class TestValidatePassword:
    def test_valid_password(self):
        assert validate_password("SecurePass1") is True

    def test_empty_raises(self):
        with pytest.raises(ValidationError, match="required"):
            validate_password("")

    def test_too_short_raises(self):
        with pytest.raises(ValidationError, match="at least"):
            validate_password("Ab1")

    def test_no_lowercase_raises(self):
        with pytest.raises(ValidationError, match="lowercase"):
            validate_password("UPPERCASE1")

    def test_no_uppercase_raises(self):
        with pytest.raises(ValidationError, match="uppercase"):
            validate_password("lowercase1")

    def test_no_digit_raises(self):
        with pytest.raises(ValidationError, match="number"):
            validate_password("NoDigitsHere")

    def test_custom_min_length(self):
        with pytest.raises(ValidationError, match="at least"):
            validate_password("Ab1xxxxx", min_length=12)


# ── Phone Validation ─────────────────────────────────────────────


class TestValidatePhone:
    def test_valid_local_format(self):
        assert validate_phone("08012345678") is True

    def test_valid_international_format(self):
        assert validate_phone("2348012345678") is True

    def test_valid_without_leading_zero(self):
        assert validate_phone("8012345678") is True

    def test_empty_raises(self):
        with pytest.raises(ValidationError, match="required"):
            validate_phone("")

    def test_invalid_format_raises(self):
        with pytest.raises(ValidationError, match="Invalid phone"):
            validate_phone("12345")


# ── Username Validation ──────────────────────────────────────────


class TestValidateUsername:
    def test_valid_username(self):
        assert validate_username("mystore123") is True

    def test_with_underscores(self):
        assert validate_username("my_store") is True

    def test_empty_raises(self):
        with pytest.raises(ValidationError, match="required"):
            validate_username("")

    def test_too_short_raises(self):
        with pytest.raises(ValidationError, match="at least 3"):
            validate_username("ab")

    def test_too_long_raises(self):
        with pytest.raises(ValidationError, match="at most 30"):
            validate_username("a" * 31)

    def test_special_chars_raises(self):
        with pytest.raises(ValidationError, match="letters, numbers"):
            validate_username("my-store!")

    def test_leading_underscore_raises(self):
        with pytest.raises(ValidationError, match="cannot start"):
            validate_username("_mystore")

    def test_trailing_underscore_raises(self):
        with pytest.raises(ValidationError, match="cannot start or end"):
            validate_username("mystore_")

    def test_reserved_username_raises(self):
        with pytest.raises(ValidationError, match="not available"):
            validate_username("admin")

    def test_reserved_username_case_insensitive(self):
        with pytest.raises(ValidationError, match="not available"):
            validate_username("Admin")


# ── Account Number Validation ────────────────────────────────────


class TestValidateAccountNumber:
    def test_valid_account(self):
        assert validate_account_number("1234567890") is True

    def test_with_spaces(self):
        assert validate_account_number("12 34 56 78 90") is True

    def test_empty_raises(self):
        with pytest.raises(ValidationError, match="required"):
            validate_account_number("")

    def test_wrong_length_raises(self):
        with pytest.raises(ValidationError, match="10 digits"):
            validate_account_number("12345")

    def test_non_digits_raises(self):
        with pytest.raises(ValidationError, match="10 digits"):
            validate_account_number("123456789a")


# ── Price Validation ─────────────────────────────────────────────


class TestValidatePrice:
    def test_valid_price(self):
        assert validate_price(1500.00) is True

    def test_zero_price(self):
        assert validate_price(0) is True

    def test_negative_raises(self):
        with pytest.raises(ValidationError, match="negative"):
            validate_price(-100)

    def test_exceeds_max_raises(self):
        with pytest.raises(ValidationError, match="exceeds"):
            validate_price(200_000_000)


# ── Quantity Validation ──────────────────────────────────────────


class TestValidateQuantity:
    def test_valid_quantity(self):
        assert validate_quantity(100) is True

    def test_zero_quantity(self):
        assert validate_quantity(0) is True

    def test_negative_raises(self):
        with pytest.raises(ValidationError, match="negative"):
            validate_quantity(-1)

    def test_exceeds_max_raises(self):
        with pytest.raises(ValidationError, match="exceeds"):
            validate_quantity(2_000_000)


# ── Image URL Validation ─────────────────────────────────────────


class TestValidateImageUrl:
    def test_empty_is_ok(self):
        assert validate_image_url("") is True

    def test_valid_jpeg_url(self):
        assert validate_image_url("https://example.com/img.jpg") is True

    def test_valid_png_url(self):
        assert validate_image_url("https://example.com/img.png") is True

    def test_cloudinary_url(self):
        assert validate_image_url(
            "https://res.cloudinary.com/demo/image/upload/sample"
        ) is True

    def test_invalid_url_raises(self):
        with pytest.raises(ValidationError, match="Invalid URL"):
            validate_image_url("not-a-url")

    def test_non_image_url_raises(self):
        with pytest.raises(ValidationError, match="valid image"):
            validate_image_url("https://example.com/file.pdf")
