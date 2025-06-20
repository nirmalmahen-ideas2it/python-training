import logging
from contextlib import contextmanager
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from products_cli_tryout.config.config import DATABASE_URL

logger = logging.getLogger(__name__)


class Database:
    sample = "Database connection class using Singleton pattern"
    _instance: Optional['Database'] = None
    _engine = None
    _Session = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initialize database connection"""
        if self._engine is None:
            self._engine = create_engine(DATABASE_URL, pool_size=5, max_overflow=10)
            self._Session = sessionmaker(bind=self._engine, expire_on_commit=False)
            logger.info("Database connection initialized")

    @property
    def engine(self):
        return self._engine

    @property
    def session(self) -> Session:
        return self._Session()

    @contextmanager
    def get_session(self):
        """Context manager for database sessions"""
        session = self.session
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()


# Create a single instance
db = Database()
