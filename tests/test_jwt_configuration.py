"""Check runtime JWT configuration in an isolated interpreter."""

import os
from pathlib import Path
import secrets
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]


def import_auth(env, extra=""):
    # Disable .env loading so each case controls the entire configuration.
    code = (
        "from unittest.mock import patch\n"
        "with patch('dotenv.load_dotenv'):\n"
        "    from utils.utils import SECRET_KEY, create_access_token, decode_access_token\n"
        + extra
    )
    return subprocess.run(
        [sys.executable, "-c", code], cwd=ROOT, env=env,
        capture_output=True, text=True, timeout=60,
    )


@pytest.mark.parametrize("value", [None, "", "   "])
def test_jwt_secret_is_required(value):
    env = {**os.environ, "DATABASE_URL": "sqlite:///:memory:"}
    env.pop("JWT_SECRET_KEY", None)
    if value is not None:
        env["JWT_SECRET_KEY"] = value
    result = import_auth(env)
    assert result.returncode != 0
    assert "JWT_SECRET_KEY" in result.stderr
    assert "RuntimeError" in result.stderr


def test_jwt_signing_uses_the_configured_secret():
    env = {
        **os.environ, "DATABASE_URL": "sqlite:///:memory:",
        "JWT_SECRET_KEY": secrets.token_urlsafe(32),
    }
    result = import_auth(env, (
        "    import os, jwt\n"
        "    token = create_access_token({'sub': 'configuration_test'})\n"
        "    assert jwt.decode(token, os.environ['JWT_SECRET_KEY'], algorithms=['HS256'])['sub'] == 'configuration_test'\n"
        "    assert decode_access_token(token)['sub'] == 'configuration_test'\n"
    ))
    assert result.returncode == 0, result.stderr
