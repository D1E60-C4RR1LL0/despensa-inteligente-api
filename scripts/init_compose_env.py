"""Generate a local Compose configuration without overwriting existing files."""

import argparse
import os
from pathlib import Path
import secrets


def create_env(path):
    password = secrets.token_urlsafe(32)
    content = (
        "# Configuracion local generada; no versionar ni compartir.\n"
        "MYSQL_DATABASE=inventory\n"
        "MYSQL_USER=inventory\n"
        "API_PORT=8000\n"
        f"MYSQL_PASSWORD={password}\n"
        f"MYSQL_ROOT_PASSWORD={secrets.token_urlsafe(32)}\n"
        f"JWT_SECRET_KEY={secrets.token_urlsafe(32)}\n"
        f"COMPOSE_DATABASE_URL=mysql+pymysql://inventory:{password}@db/inventory\n"
    )
    # Exclusive creation also protects against overwrites by concurrent runs.
    try:
        descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError:
        return False
    with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as target:
        target.write(content)
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).resolve().parents[1] / ".env.compose")
    args = parser.parse_args()
    if create_env(args.output):
        print("Configuracion Compose creada. Los secretos no se muestran.")
    else:
        print("El archivo ya existe; se conservo sin modificaciones.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
