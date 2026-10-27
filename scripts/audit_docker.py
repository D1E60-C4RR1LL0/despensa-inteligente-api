"""Check the API image over HTTP using a disposable MySQL container.

Build inventory-api:e2-docker and pull mysql:8.4 before running this script.
Existing databases and host configuration files are never mounted or used.
"""

import argparse
from http.client import HTTPException
import json
import os
import secrets
import subprocess
import sys
import time
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


def docker(*args, env=None, check=True):
    return subprocess.run(
        ["docker", *args], env=env, capture_output=True,
        text=True, check=check, timeout=60,
    )


def request(base, path, payload=None, token=None, form=False):
    headers = {}
    data = None
    if payload is not None:
        data = (urlencode(payload) if form else json.dumps(payload)).encode()
        headers["Content-Type"] = (
            "application/x-www-form-urlencoded" if form else "application/json"
        )
    if token:
        headers["Authorization"] = "Bearer " + token
    with urlopen(Request(base + path, data=data, headers=headers), timeout=5) as response:
        return json.load(response)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", default="inventory-api:e2-docker")
    args = parser.parse_args()
    image = json.loads(docker("image", "inspect", args.image).stdout)[0]
    identity = json.loads(docker("run", "--rm", "--pull=never", args.image,
        "python", "-c", (
            "import importlib.util,json,os; from pathlib import Path; "
            "print(json.dumps({'uid':os.getuid(), "
            "'pytest_installed':importlib.util.find_spec('pytest') is not None, "
            "'excluded_files_absent':all(not (Path('/app') / p).exists() "
            "for p in ['.env','.env.example','.git','venv','tests','ci.db','.coverage'])}))"
        )).stdout)
    assert identity["uid"] != 0, "La imagen ejecuta como root"
    assert not identity["pytest_installed"], "PyTest no debe estar en la imagen"
    assert identity["excluded_files_absent"], "La imagen contiene archivos locales"

    network = None
    containers = []
    suffix = secrets.token_hex(6)
    password = secrets.token_urlsafe(32)
    env = {
        **os.environ,
        "MYSQL_ROOT_PASSWORD": secrets.token_urlsafe(32),
        "MYSQL_DATABASE": "docker_audit",
        "MYSQL_USER": "docker_audit",
        "MYSQL_PASSWORD": password,
        "DATABASE_URL": f"mysql+pymysql://docker_audit:{password}@db/docker_audit",
        "JWT_SECRET_KEY": secrets.token_urlsafe(32),
    }
    try:
        network = docker("network", "create", "--label", "inventory-api.audit=docker",
                         "inventory-docker-" + suffix).stdout.strip()
        database = docker(
            "run", "--detach", "--rm", "--pull=never",
            "--name", "inventory-db-" + suffix,
            "--label", "inventory-api.audit=docker",
            "--network", network, "--network-alias", "db",
            "--tmpfs", "/var/lib/mysql",
            "--env", "MYSQL_ROOT_PASSWORD", "--env", "MYSQL_DATABASE",
            "--env", "MYSQL_USER", "--env", "MYSQL_PASSWORD",
            "mysql:8.4", env=env,
        ).stdout.strip()
        containers.append(database)
        deadline = time.monotonic() + 120
        while True:
            ready = docker("exec", database, "sh", "-c",
                'MYSQL_PWD="$MYSQL_PASSWORD" mysql --protocol=TCP -h127.0.0.1 '
                '-u"$MYSQL_USER" "$MYSQL_DATABASE" -Nse "SELECT VERSION()"',
                check=False)
            if ready.returncode == 0:
                mysql_version = ready.stdout.strip()
                break
            if time.monotonic() > deadline:
                raise RuntimeError("El MySQL temporal no estuvo listo en 120 segundos")
            time.sleep(1)
        print("MySQL temporal listo: " + mysql_version, flush=True)

        docker("run", "--rm", "--pull=never", "--network", network,
               "--env", "DATABASE_URL", "--env", "JWT_SECRET_KEY",
               args.image, "python", "-m", "alembic", "upgrade", "head", env=env)
        api = docker(
            "run", "--detach", "--rm", "--pull=never",
            "--name", "inventory-api-" + suffix,
            "--label", "inventory-api.audit=docker",
            "--network", network, "--publish", "127.0.0.1::8000",
            "--env", "DATABASE_URL", "--env", "JWT_SECRET_KEY",
            args.image, env=env,
        ).stdout.strip()
        containers.append(api)
        ports = json.loads(docker("inspect", "--format",
                                 '{{json .NetworkSettings.Ports}}', api).stdout)
        base = "http://127.0.0.1:" + ports["8000/tcp"][0]["HostPort"]
        deadline = time.monotonic() + 60
        while True:
            try:
                specification = request(base, "/openapi.json")
                break
            except (URLError, HTTPException, ConnectionError, TimeoutError):
                if time.monotonic() > deadline:
                    raise RuntimeError("La API no estuvo lista en 60 segundos") from None
                time.sleep(1)

        signup = request(base, "/signup", {
            "username": "docker_audit", "email": "docker_audit@example.com",
            "first_name": "Docker", "last_name": "Audit",
            "password": password, "role": "user",
        })
        login = request(base, "/login", {"username": "docker_audit", "password": password},
                        form=True)
        token = login["access_token"]
        checks = {
            "openapi": "/login" in specification["paths"],
            "signup": signup["username"] == "docker_audit",
            "login": login["token_type"] == "bearer" and bool(token),
        }
        for path in ("/productos/", "/stocks/", "/stocks/alertas", "/productos/lista-compras"):
            checks[path] = request(base, path, token=token) == []

        deadline = time.monotonic() + 60
        while True:
            health = docker("inspect", "--format", '{{.State.Health.Status}}', api).stdout.strip()
            if health == "healthy":
                break
            if time.monotonic() > deadline:
                raise RuntimeError("El healthcheck de la API no llego a healthy")
            time.sleep(1)
        report = {
            "image": args.image, "image_id": image["Id"],
            "image_size_bytes": image["Size"], "identity": identity,
            "mysql_version": mysql_version, "health": health,
            "api_checks": checks, "all_checks_pass": all(checks.values()),
        }
        print(json.dumps(report, indent=2))
        return 0 if all(checks.values()) else 1
    finally:
        for container in reversed(containers):
            docker("rm", "--force", container, check=False)
        if network:
            docker("network", "rm", network)
        print("Recursos temporales de la auditoria eliminados.", flush=True)


if __name__ == "__main__":
    sys.exit(main())
