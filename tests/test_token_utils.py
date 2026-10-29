"""Isolated checks for JWT expiry, signatures and malformed credentials."""

from datetime import timedelta
import secrets

import jwt
import pytest

from utils.utils import create_access_token, decode_access_token


def test_valid_token_preserves_subject_without_mutating_input():
    claims = {"sub": "unit-user"}
    token = create_access_token(claims)
    assert decode_access_token(token)["sub"] == "unit-user"
    assert claims == {"sub": "unit-user"}


def test_expired_token_is_rejected():
    token = create_access_token({"sub": "unit-user"}, expires_delta=timedelta(seconds=-1))
    assert decode_access_token(token) is None


def test_token_signed_with_another_key_is_rejected():
    token = jwt.encode({"sub": "unit-user"}, secrets.token_urlsafe(32), algorithm="HS256")
    assert decode_access_token(token) is None


@pytest.mark.parametrize("token", ["not-a-jwt", "a.b.c"])
def test_malformed_token_is_rejected(token):
    assert decode_access_token(token) is None
