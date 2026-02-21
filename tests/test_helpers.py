"""
Tests for app.utils.helpers — utility functions.
"""

import json
import re

from app.utils.helpers import (
    generate_uuid,
    generate_order_number,
    generate_reference,
    generate_otp,
    format_currency,
    format_phone,
    validate_email,
    validate_phone,
    slugify,
    truncate,
    mask_email,
    mask_phone,
    mask_account_number,
    calculate_percentage,
    parse_json_safely,
    dict_to_query_string,
)


# ── UUID Generation ───────────────────────────────────────────────


class TestGenerateUUID:
    def test_returns_string(self):
        result = generate_uuid()
        assert isinstance(result, str)

    def test_unique(self):
        ids = {generate_uuid() for _ in range(100)}
        assert len(ids) == 100


# ── Order Number ──────────────────────────────────────────────────


class TestGenerateOrderNumber:
    def test_format(self):
        order_num = generate_order_number()
        assert re.match(r"^ORD-\d{8}-\d{5}$", order_num)

    def test_unique(self):
        nums = {generate_order_number() for _ in range(50)}
        # Very high probability of uniqueness
        assert len(nums) >= 45


# ── Reference ─────────────────────────────────────────────────────


class TestGenerateReference:
    def test_default_prefix(self):
        ref = generate_reference()
        assert ref.startswith("REF-")

    def test_custom_prefix(self):
        ref = generate_reference(prefix="PAY")
        assert ref.startswith("PAY-")

    def test_length(self):
        ref = generate_reference()
        # "REF-" + 10 chars = 14 total
        assert len(ref) == 14


# ── OTP Generation ────────────────────────────────────────────────


class TestGenerateOTP:
    def test_default_length(self):
        otp = generate_otp()
        assert len(otp) == 6
        assert otp.isdigit()

    def test_custom_length(self):
        otp = generate_otp(length=4)
        assert len(otp) == 4
        assert otp.isdigit()


# ── Currency Formatting ──────────────────────────────────────────


class TestFormatCurrency:
    def test_naira_default(self):
        result = format_currency(1500.50)
        assert result == "₦1,500.50"

    def test_custom_symbol(self):
        result = format_currency(1000, symbol="$")
        assert result == "$1,000.00"

    def test_zero(self):
        result = format_currency(0)
        assert result == "₦0.00"


# ── Phone Formatting ─────────────────────────────────────────────


class TestFormatPhone:
    def test_local_format(self):
        result = format_phone("08012345678")
        assert result == "2348012345678"

    def test_already_international(self):
        result = format_phone("2348012345678")
        assert result == "2348012345678"

    def test_plus_prefix(self):
        result = format_phone("+2348012345678")
        assert result == "2348012345678"


# ── Email Validation ─────────────────────────────────────────────


class TestValidateEmail:
    def test_valid_email(self):
        assert validate_email("user@example.com") is True

    def test_invalid_email(self):
        assert validate_email("not-an-email") is False

    def test_invalid_no_domain(self):
        assert validate_email("user@") is False


# ── Phone Validation ─────────────────────────────────────────────


class TestValidatePhone:
    def test_valid_local(self):
        assert validate_phone("08012345678") is True

    def test_valid_international(self):
        assert validate_phone("2348012345678") is True

    def test_invalid_short(self):
        assert validate_phone("0801234") is False


# ── Slugify ───────────────────────────────────────────────────────


class TestSlugify:
    def test_basic(self):
        assert slugify("Hello World") == "hello-world"

    def test_special_chars(self):
        assert slugify("Hello, World!") == "hello-world"

    def test_extra_spaces(self):
        assert slugify("  Hello   World  ") == "hello-world"

    def test_unicode(self):
        result = slugify("Café au Lait")
        assert isinstance(result, str)


# ── Truncate ──────────────────────────────────────────────────────


class TestTruncate:
    def test_short_text_unchanged(self):
        assert truncate("hello", length=100) == "hello"

    def test_long_text_truncated(self):
        result = truncate("a " * 100, length=20)
        assert len(result) <= 20
        assert result.endswith("...")


# ── Masking ───────────────────────────────────────────────────────


class TestMaskEmail:
    def test_standard_email(self):
        result = mask_email("sammy@gmail.com")
        assert result.startswith("s")
        assert "@gmail.com" in result
        assert "*" in result

    def test_short_local_part(self):
        result = mask_email("ab@example.com")
        assert "@example.com" in result

    def test_no_at_sign(self):
        assert mask_email("not-email") == "not-email"


class TestMaskPhone:
    def test_standard_phone(self):
        result = mask_phone("08012345678")
        assert result.startswith("080")
        assert result.endswith("678")
        assert "*" in result

    def test_short_phone(self):
        result = mask_phone("123")
        assert result == "123"


class TestMaskAccountNumber:
    def test_standard_account(self):
        result = mask_account_number("1234567890")
        assert result.startswith("123")
        assert result.endswith("890")
        assert "*" in result

    def test_short_account(self):
        assert mask_account_number("12345") == "12345"


# ── Calculate Percentage ─────────────────────────────────────────


class TestCalculatePercentage:
    def test_normal(self):
        assert calculate_percentage(25, 100) == 25.0

    def test_zero_denominator(self):
        assert calculate_percentage(10, 0) == 0


# ── JSON Parsing ─────────────────────────────────────────────────


class TestParseJsonSafely:
    def test_valid_json(self):
        result = parse_json_safely('{"key": "value"}')
        assert result == {"key": "value"}

    def test_invalid_json(self):
        result = parse_json_safely("not json", default={})
        assert result == {}

    def test_none_input(self):
        result = parse_json_safely(None, default=None)
        assert result is None


# ── Query String ──────────────────────────────────────────────────


class TestDictToQueryString:
    def test_basic(self):
        result = dict_to_query_string({"a": "1", "b": "2"})
        assert "a=1" in result
        assert "b=2" in result

    def test_none_values_excluded(self):
        result = dict_to_query_string({"a": "1", "b": None})
        assert "a=1" in result
        assert "b" not in result
