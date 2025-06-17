from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import logging
from config import DATABASE_URL

logger = logging.getLogger(__name__)

# Create engine with connection pooling
engine = create_engine(DATABASE_URL, pool_size=5, max_overflow=10)
Session = sessionmaker(bind=engine)
