"""
SQLite to PostgreSQL Migration Script with Serialization & Logging

Author: Simeon J R
Date: 2026-04-23

Description:
    Migrates data from SQLite to PostgreSQL using SQLAlchemy ORM with:
    - Batch processing
    - Serialization layer for type safety
    - Structured logging (file + console)
    - Error handling and retry support

Usage:
    python migrate.py

Requirements:
    pip install sqlalchemy psycopg2-binary
"""
import os
import logging
import sys
import time
from datetime import datetime, date
from typing import Dict, Any, List

from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError


# =========================
# CONFIGURATION
# =========================
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLITE_DB_URL = f"sqlite:///{os.path.join(BASE_DIR, 'Database', 'MovieInfo.db')}" #"sqlite:///source.db"
POSTGRES_DB_URL = "postgresql+psycopg2://postgres:jrs%23321@localhost:5432/inapp_db"

BATCH_SIZE = 2000
MAX_RETRIES = 3
LOG_FILE = "migration.log"


# =========================
# LOGGING SETUP
# =========================
def setup_logging() -> None:
    """
    Configure logging for both console and file output.
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    # Console handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)

    # File handler
    fh = logging.FileHandler(LOG_FILE)
    fh.setFormatter(formatter)

    logger.addHandler(ch)
    logger.addHandler(fh)


# =========================
# SERIALIZATION
# =========================
def serialize_row(row) -> Dict[str, Any]:
    """
    Convert SQLAlchemy row object into a serializable dictionary.

    Args:
        row: SQLAlchemy row result

    Returns:
        dict: Serialized row
    """
    result = {}

    for key, value in row._mapping.items():
        if isinstance(value, (datetime, date)):
            result[key] = value.isoformat()

        elif isinstance(value, bytes):
            result[key] = value.decode("utf-8", errors="ignore")

        elif value == "":
            result[key] = None

        else:
            result[key] = value

    return result


def transform_for_postgres(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Apply transformations to ensure PostgreSQL compatibility.

    Args:
        data: Serialized row

    Returns:
        dict: Transformed row
    """
    for key, value in data.items():
        if isinstance(value, str):
            if value.lower() == "true":
                data[key] = True
            elif value.lower() == "false":
                data[key] = False

    return data


# =========================
# MIGRATION LOGIC
# =========================
def migrate_table(
    table: Table,
    sqlite_session,
    postgres_session
) -> None:
    """
    Migrate a single table from SQLite to PostgreSQL.

    Args:
        table: SQLAlchemy Table object
        sqlite_session: Source DB session
        postgres_session: Target DB session
    """
    logger = logging.getLogger()
    offset = 0

    logger.info(f"Starting migration for table: {table.name}")

    while True:
        try:
            rows = sqlite_session.execute(
                table.select().limit(BATCH_SIZE).offset(offset)
            ).fetchall()

            if not rows:
                break

            batch: List[Dict[str, Any]] = []

            for row in rows:
                data = serialize_row(row)
                data = transform_for_postgres(data)
                batch.append(data)

            retry_count = 0

            while retry_count < MAX_RETRIES:
                try:
                    # postgres_session.bulk_insert_mappings(table, batch)
                    # postgres_session.commit()
                    postgres_session.execute(table.insert(), batch)
                    postgres_session.commit()
                    break

                except SQLAlchemyError as e:
                    retry_count += 1
                    logger.error(
                        f"Retry {retry_count} failed for table {table.name}: {e}"
                    )
                    time.sleep(2)

            if retry_count == MAX_RETRIES:
                logger.error(
                    f"Max retries reached. Skipping batch at offset {offset}"
                )
                continue

            offset += BATCH_SIZE
            logger.info(f"{table.name}: Inserted {offset} rows")

        except Exception as e:
            logger.exception(
                f"Critical error in table {table.name} at offset {offset}: {e}"
            )
            break

    logger.info(f"Completed migration for table: {table.name}")


# =========================
# MAIN EXECUTION
# =========================
def main() -> None:
    """
    Main function to execute migration.
    """
    setup_logging()
    logger = logging.getLogger()

    logger.info("Starting SQLite → PostgreSQL migration")

    try:
        # Engines
        sqlite_engine = create_engine(SQLITE_DB_URL)
        postgres_engine = create_engine(POSTGRES_DB_URL)


        # Reflect schema
        metadata = MetaData()
        metadata.reflect(bind=sqlite_engine)

        # Create tables in Postgres
        metadata.create_all(postgres_engine)

        # Sessions
        SQLiteSession = sessionmaker(bind=sqlite_engine)
        PostgresSession = sessionmaker(bind=postgres_engine)

        sqlite_session = SQLiteSession()
        postgres_session = PostgresSession()

        # Migrate each table
        for table in metadata.tables.values():
            migrate_table(table, sqlite_session, postgres_session)

        logger.info("Migration completed successfully!")

    except Exception as e:
        logger.exception(f"Migration failed: {e}")


if __name__ == "__main__":
    main()