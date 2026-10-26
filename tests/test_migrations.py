"""Regression checks against independent databases, without API test fixtures."""

import os
from pathlib import Path
import subprocess
import sys

from alembic.autogenerate import compare_metadata
from alembic.migration import MigrationContext
import pytest
from sqlalchemy import create_engine, inspect, text

from config.database import Base


ROOT = Path(__file__).resolve().parents[1]
PREVIOUS_REVISION = "0c11a0e481fc"


@pytest.fixture
def migration_database(tmp_path):
    url = "sqlite:///" + (tmp_path / "migrations.db").as_posix()
    engine = create_engine(url)
    env = {**os.environ, "DATABASE_URL": url}
    yield engine, env
    engine.dispose()


def run_alembic(env, *args):
    return subprocess.run(
        [sys.executable, "-m", "alembic", *args],
        cwd=ROOT, env=env, capture_output=True, text=True, timeout=60,
    )


def upgrade(env, revision="head"):
    result = run_alembic(env, "upgrade", revision)
    assert result.returncode == 0, result.stdout + result.stderr


def assert_models_match(engine):
    with engine.connect() as connection:
        assert compare_metadata(
            MigrationContext.configure(connection), Base.metadata
        ) == []


def test_migrations_rebuild_schema_and_preserve_existing_users(migration_database):
    engine, env = migration_database
    upgrade(env, PREVIOUS_REVISION)
    with engine.begin() as connection:
        connection.execute(text(
            "INSERT INTO users (username) VALUES ('migration_sentinel')"
        ))

    upgrade(env)
    assert_models_match(engine)
    upgrade(env)  # Re-running migrations must not recreate tables or lose data.
    result = run_alembic(env, "downgrade", PREVIOUS_REVISION)
    assert result.returncode == 0, result.stdout + result.stderr
    assert set(inspect(engine).get_table_names()) == {
        "alembic_version", "users", "token_blacklist",
    }
    upgrade(env)
    assert_models_match(engine)
    with engine.connect() as connection:
        assert connection.execute(text(
            "SELECT username FROM users"
        )).scalars().all() == ["migration_sentinel"]


def test_legacy_collision_stops_before_creating_other_tables(migration_database):
    engine, env = migration_database
    upgrade(env, PREVIOUS_REVISION)
    with engine.begin() as connection:
        connection.execute(text("CREATE TABLE stocks (id INTEGER PRIMARY KEY)"))
        connection.execute(text("INSERT INTO stocks (id) VALUES (7)"))

    before = set(inspect(engine).get_table_names())
    result = run_alembic(env, "upgrade", "head")
    assert result.returncode != 0
    assert "Existen tablas de inventario" in result.stderr
    assert set(inspect(engine).get_table_names()) == before
    with engine.connect() as connection:
        assert connection.execute(text("SELECT id FROM stocks")).scalar_one() == 7
        assert connection.execute(text(
            "SELECT version_num FROM alembic_version"
        )).scalar_one() == PREVIOUS_REVISION


def test_importing_app_does_not_create_tables(migration_database):
    engine, env = migration_database
    assert inspect(engine).get_table_names() == []
    result = subprocess.run(
        [sys.executable, "-c", "import app"],
        cwd=ROOT, env=env, capture_output=True, text=True, timeout=60,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert inspect(engine).get_table_names() == []


def test_matching_legacy_schema_can_be_stamped_without_losing_data(migration_database):
    engine, env = migration_database
    upgrade(env, PREVIOUS_REVISION)
    Base.metadata.create_all(engine)  # Reproduce the previous application's schema.
    with engine.begin() as connection:
        connection.execute(text(
            "INSERT INTO categorias (nombre) VALUES ('legacy_sentinel')"
        ))
    check = subprocess.run(
        [sys.executable, "scripts/check_schema.py"],
        cwd=ROOT, env=env, capture_output=True, text=True, timeout=60,
    )
    assert check.returncode == 0, check.stdout + check.stderr
    result = run_alembic(env, "stamp", "f3171e47e124")
    assert result.returncode == 0, result.stdout + result.stderr
    upgrade(env)
    assert_models_match(engine)
    with engine.connect() as connection:
        assert connection.execute(text(
            "SELECT nombre FROM categorias"
        )).scalars().all() == ["legacy_sentinel"]
