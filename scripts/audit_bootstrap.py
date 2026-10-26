"""Audit migrations and API startup using a disposable SQLite or MySQL database.

Exit with 1 when migrations do not reproduce the models or API checks fail.
Never use the database configured in the user's environment or .env file.
"""

import argparse
import json
import os
from pathlib import Path
import secrets
import subprocess
import sys
from tempfile import TemporaryDirectory
import time


def audit_database(database_url, label):
    root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(root))
    os.environ["DATABASE_URL"] = database_url

    def migrate(*args):
        result = subprocess.run(
            [sys.executable, "-m", "alembic", *args],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=60,
        )
        if result.returncode:
            print(result.stdout)
            print(result.stderr, file=sys.stderr)
            raise RuntimeError("Fallo en la comprobacion de migraciones")
        return result.returncode

    migration_exit = migrate("upgrade", "head")
    # Compare the migrated schema before importing the application.
    import models  # noqa: F401
    from config.database import Base, engine
    from alembic.autogenerate import compare_metadata
    from alembic.migration import MigrationContext
    from sqlalchemy import inspect, text

    try:
        expected = set(Base.metadata.tables)
        migrated = set(inspect(engine).get_table_names())
        with engine.connect() as connection:
            revision = connection.execute(
                text("SELECT version_num FROM alembic_version")
            ).scalar_one()
            differences = compare_metadata(
                MigrationContext.configure(connection), Base.metadata
            )

        from app import app
        from fastapi.testclient import TestClient

        started = set(inspect(engine).get_table_names())
        migrate("upgrade", "head")
        checks = {}
        password = secrets.token_urlsafe(24)
        with TestClient(app) as client:
            response = client.get("/openapi.json")
            checks["openapi"] = response.status_code == 200
            response = client.post("/signup", json={
                "username": "bootstrap_audit",
                "email": "bootstrap@example.com",
                "first_name": "Bootstrap",
                "last_name": "Audit",
                "password": password,
                "role": "user",
            })
            checks["signup"] = response.status_code == 200
            response = client.post("/login", data={
                "username": "bootstrap_audit", "password": password,
            })
            token = response.json().get("access_token")
            checks["login"] = response.status_code == 200 and bool(token)
            headers = {"Authorization": f"Bearer {token}"} if token else {}
            for path in ("/productos/", "/stocks/", "/stocks/alertas",
                         "/productos/lista-compras"):
                response = client.get(path, headers=headers)
                checks[path] = (
                    response.status_code == 200 and response.json() == []
                )

        report = {
            "database": label,
            "alembic_upgrade_exit": migration_exit,
            "alembic_revision": revision,
            "expected_model_tables": sorted(expected),
            "tables_after_migrations": sorted(migrated),
            "missing_after_migrations": sorted(expected - migrated),
            "schema_difference_count": len(differences),
            "tables_created_on_app_import": sorted(started - migrated),
            "app_preserves_schema": started == migrated,
            "api_checks": checks,
            "migrations_match_models": not differences,
            "api_checks_pass": all(checks.values()),
        }
        # Only this disposable database is rolled back; users must survive.
        migrate("downgrade", "0c11a0e481fc")
        with engine.connect() as connection:
            user_survives = connection.execute(text(
                "SELECT COUNT(*) FROM users WHERE username = 'bootstrap_audit'"
            )).scalar_one() == 1
        migrate("upgrade", "head")
        with engine.connect() as connection:
            roundtrip_differences = compare_metadata(
                MigrationContext.configure(connection), Base.metadata
            )
        report["migration_roundtrip_pass"] = (
            user_survives and not roundtrip_differences
        )
        print(json.dumps(report, indent=2))
        return 0 if (
            not differences and started == migrated and all(checks.values())
            and report["migration_roundtrip_pass"]
        ) else 1
    finally:
        engine.dispose()


def audit_mysql():
    """Create and remove only our own container, never an existing database."""
    def docker(*args, env=None):
        return subprocess.run(
            ["docker", *args], env=env, check=True, capture_output=True,
            text=True, timeout=60,
        ).stdout.strip()

    container = None
    password = secrets.token_urlsafe(32)
    env = {
        **os.environ,
        "MYSQL_ROOT_PASSWORD": secrets.token_urlsafe(32),
        "MYSQL_DATABASE": "bootstrap_audit",
        "MYSQL_USER": "bootstrap_audit",
        "MYSQL_PASSWORD": password,
    }
    try:
        container = docker(
            "run", "--detach", "--rm", "--pull=never",
            "--name", "inventory-bootstrap-" + secrets.token_hex(6),
            "--label", "inventory-api.audit=bootstrap",
            "--tmpfs", "/var/lib/mysql",
            "--publish", "127.0.0.1::3306",
            "--env", "MYSQL_ROOT_PASSWORD", "--env", "MYSQL_DATABASE",
            "--env", "MYSQL_USER", "--env", "MYSQL_PASSWORD",
            "mysql:8.4", env=env,
        )
        from sqlalchemy import create_engine, text
        from sqlalchemy.engine import URL
        from sqlalchemy.exc import OperationalError

        port = json.loads(docker("inspect", "--format",
                                '{{json .NetworkSettings.Ports}}', container))
        url = URL.create(
            "mysql+pymysql", username=env["MYSQL_USER"], password=password,
            host="127.0.0.1", port=int(port["3306/tcp"][0]["HostPort"]),
            database=env["MYSQL_DATABASE"], query={"connect_timeout": "3"},
        )
        probe = create_engine(url)
        try:
            deadline = time.monotonic() + 120
            while True:
                try:
                    with probe.connect() as connection:
                        version = connection.execute(text("SELECT VERSION()")).scalar_one()
                    break
                except OperationalError:
                    if time.monotonic() >= deadline:
                        raise RuntimeError("MySQL temporal no estuvo listo en 120 segundos") from None
                    time.sleep(1)
        finally:
            probe.dispose()
        print("MySQL temporal listo. Version: " + version, flush=True)
        return audit_database(url.render_as_string(hide_password=False),
                              "disposable MySQL " + version)
    finally:
        if container:
            docker("rm", "--force", container)
            print("Contenedor MySQL temporal eliminado.", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mysql", action="store_true",
                        help="Use a temporary Docker container with mysql:8.4")
    args = parser.parse_args()
    if args.mysql:
        return audit_mysql()
    root = Path(__file__).resolve().parents[1]
    scratch = root / ".pytest_cache"
    scratch.mkdir(exist_ok=True)
    with TemporaryDirectory(prefix="bootstrap-", dir=scratch) as temporary:
        database = Path(temporary) / "audit.db"
        return audit_database("sqlite:///" + database.as_posix(), "disposable SQLite")


if __name__ == "__main__":
    sys.exit(main())
