"""Compare the configured database with the models without changing its schema."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from alembic.autogenerate import compare_metadata
from alembic.migration import MigrationContext
import models  # noqa: F401
from config.database import Base, engine


def main():
    try:
        with engine.connect() as connection:
            differences = compare_metadata(
                MigrationContext.configure(connection), Base.metadata
            )
        print(f"Diferencias de esquema detectadas por Alembic: {len(differences)}")
        for difference in differences:
            print(repr(difference))
        return 1 if differences else 0
    finally:
        engine.dispose()


if __name__ == "__main__":
    sys.exit(main())
