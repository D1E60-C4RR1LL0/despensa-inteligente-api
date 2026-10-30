"""Protect local credentials from overwrites and inconsistent generated URLs."""

from dotenv import dotenv_values
from sqlalchemy.engine import make_url

from scripts.init_compose_env import create_env


def test_existing_compose_configuration_is_not_overwritten(tmp_path):
    path = tmp_path / ".env.compose"
    original = b"# configuracion propia\nAPI_PORT=9123\n"
    path.write_bytes(original)
    assert create_env(path) is False
    assert path.read_bytes() == original


def test_generated_credentials_match_database_url_and_are_independent(tmp_path):
    first = tmp_path / ".env.first"
    second = tmp_path / ".env.second"
    assert create_env(first) is True
    assert create_env(second) is True
    values = dotenv_values(first)
    other = dotenv_values(second)
    url = make_url(values["COMPOSE_DATABASE_URL"])
    assert url.host == "db"
    assert url.username == values["MYSQL_USER"]
    assert url.database == values["MYSQL_DATABASE"]
    assert url.password == values["MYSQL_PASSWORD"]
    keys = ("MYSQL_PASSWORD", "MYSQL_ROOT_PASSWORD", "JWT_SECRET_KEY")
    assert len({values[key] for key in keys}) == 3
    for key in keys:
        assert len(values[key]) >= 32
        assert values[key] != other[key]
