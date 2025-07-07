"""
Database configuration and session management
"""

import time
from contextlib import contextmanager
from sqlalchemy import event
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from typing import Generator
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

# Database engine configuration
if settings.DATABASE_URL.startswith("sqlite"):
    # SQLite configuration for development
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={
            "check_same_thread": False,
            "timeout": 20,
        },
        poolclass=StaticPool,
        echo=settings.DEBUG,
    )
else:
    # PostgreSQL configuration for production
    engine = create_engine(
        settings.DATABASE_URL,
        pool_size=settings.DATABASE_POOL_SIZE,
        max_overflow=settings.DATABASE_MAX_OVERFLOW,
        pool_timeout=settings.DATABASE_POOL_TIMEOUT,
        pool_recycle=3600,
        echo=settings.DEBUG,
    )

# Session configuration
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False
)

# Base class for models
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Database session dependency
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def create_tables():
    """Create all database tables"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise


def drop_tables():
    """Drop all database tables"""
    try:
        Base.metadata.drop_all(bind=engine)
        logger.info("Database tables dropped successfully")
    except Exception as e:
        logger.error(f"Error dropping database tables: {e}")
        raise


def check_db_connection():
    """Check database connection"""
    try:
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        logger.info("Database connection successful")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False

# Database utilities


class DatabaseManager:
    """Database management utilities"""

    def __init__(self):
        self.engine = engine
        self.SessionLocal = SessionLocal

    def create_session(self) -> Session:
        """Create a new database session"""
        return self.SessionLocal()

    def execute_raw_query(self, query: str, params: dict = None):
        """Execute raw SQL query"""
        with self.engine.connect() as conn:
            result = conn.execute(query, params or {})
            return result.fetchall()

    def get_table_info(self, table_name: str):
        """Get table information"""
        query = f"""
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns
        WHERE table_name = '{table_name}'
        ORDER BY ordinal_position;
        """
        return self.execute_raw_query(query)

    def get_database_size(self):
        """Get database size"""
        if settings.DATABASE_URL.startswith("sqlite"):
            import os
            db_path = settings.DATABASE_URL.replace("sqlite:///", "")
            return os.path.getsize(db_path) if os.path.exists(db_path) else 0
        else:
            query = """
            SELECT pg_size_pretty(pg_database_size(current_database())) as size;
            """
            result = self.execute_raw_query(query)
            return result[0][0] if result else "Unknown"

    def vacuum_database(self):
        """Vacuum database to reclaim space"""
        if settings.DATABASE_URL.startswith("sqlite"):
            with self.engine.connect() as conn:
                conn.execute("VACUUM")
        else:
            with self.engine.connect() as conn:
                conn.execute("VACUUM ANALYZE")

    def backup_database(self, backup_path: str):
        """Backup database"""
        if settings.DATABASE_URL.startswith("sqlite"):
            import shutil
            db_path = settings.DATABASE_URL.replace("sqlite:///", "")
            shutil.copy2(db_path, backup_path)
        else:
            # For PostgreSQL, use pg_dump
            import subprocess
            cmd = [
                "pg_dump",
                settings.DATABASE_URL,
                "-f", backup_path,
                "--verbose"
            ]
            subprocess.run(cmd, check=True)

    def restore_database(self, backup_path: str):
        """Restore database from backup"""
        if settings.DATABASE_URL.startswith("sqlite"):
            import shutil
            db_path = settings.DATABASE_URL.replace("sqlite:///", "")
            shutil.copy2(backup_path, db_path)
        else:
            # For PostgreSQL, use pg_restore
            import subprocess
            cmd = [
                "pg_restore",
                "-d", settings.DATABASE_URL,
                backup_path,
                "--verbose"
            ]
            subprocess.run(cmd, check=True)


# Global database manager instance
db_manager = DatabaseManager()

# Connection pool monitoring


def get_pool_status():
    """Get database connection pool status"""
    pool = engine.pool
    return {
        "size": pool.size(),
        "checked_in": pool.checkedin(),
        "checked_out": pool.checkedout(),
        "overflow": pool.overflow(),
        "invalid": pool.invalid(),
    }

# Database health check


def health_check():
    """Comprehensive database health check"""
    try:
        with engine.connect() as conn:
            # Basic connection test
            conn.execute("SELECT 1")

            # Check if we can read from main tables
            conn.execute("SELECT COUNT(*) FROM scholarships LIMIT 1")

            # Check connection pool
            pool_status = get_pool_status()

            return {
                "status": "healthy",
                "connection": "ok",
                "pool": pool_status,
                "database_size": db_manager.get_database_size()
            }
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }

# Migration utilities


class MigrationManager:
    """Database migration utilities"""

    def __init__(self):
        self.engine = engine

    def create_migration_table(self):
        """Create migrations tracking table"""
        query = """
        CREATE TABLE IF NOT EXISTS migrations (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL UNIQUE,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        with self.engine.connect() as conn:
            conn.execute(query)

    def get_applied_migrations(self):
        """Get list of applied migrations"""
        query = "SELECT name FROM migrations ORDER BY applied_at"
        with self.engine.connect() as conn:
            result = conn.execute(query)
            return [row[0] for row in result.fetchall()]

    def mark_migration_applied(self, migration_name: str):
        """Mark migration as applied"""
        query = "INSERT INTO migrations (name) VALUES (:name)"
        with self.engine.connect() as conn:
            conn.execute(query, {"name": migration_name})

    def rollback_migration(self, migration_name: str):
        """Rollback migration"""
        query = "DELETE FROM migrations WHERE name = :name"
        with self.engine.connect() as conn:
            conn.execute(query, {"name": migration_name})


# Global migration manager instance
migration_manager = MigrationManager()

# Database events


@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Set SQLite pragmas for better performance"""
    if settings.DATABASE_URL.startswith("sqlite"):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA synchronous=NORMAL")
        cursor.execute("PRAGMA cache_size=1000")
        cursor.execute("PRAGMA temp_store=MEMORY")
        cursor.close()


@event.listens_for(engine, "before_cursor_execute")
def receive_before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    """Log slow queries"""
    if settings.DEBUG:
        context._query_start_time = time.time()


@event.listens_for(engine, "after_cursor_execute")
def receive_after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    """Log query execution time"""
    if settings.DEBUG:
        total = time.time() - context._query_start_time
        if total > 0.1:  # Log queries taking more than 100ms
            logger.warning(f"Slow query: {total:.2f}s - {statement[:100]}...")


# Database transaction utilities


@contextmanager
def db_transaction():
    """Database transaction context manager"""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Transaction failed: {e}")
        raise
    finally:
        db.close()


# Async database utilities (for future use)
try:
    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
    from sqlalchemy.orm import sessionmaker as async_sessionmaker

    # Async engine for future async operations
    if not settings.DATABASE_URL.startswith("sqlite"):
        async_database_url = settings.DATABASE_URL.replace(
            "postgresql://", "postgresql+asyncpg://")
        async_engine = create_async_engine(
            async_database_url, echo=settings.DEBUG)
        AsyncSessionLocal = async_sessionmaker(
            async_engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
    else:
        async_engine = None
        AsyncSessionLocal = None

except ImportError:
    # Async dependencies not available
    async_engine = None
    AsyncSessionLocal = None


async def get_async_db():
    """Async database session dependency"""
    if AsyncSessionLocal is None:
        raise RuntimeError("Async database not configured")

    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            logger.error(f"Async database session error: {e}")
            raise
        finally:
            await session.close()
