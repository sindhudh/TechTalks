import datetime
import os

from sqlalchemy import create_engine, Column, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import config

# Define the base class for declarative class definitions
Base = declarative_base()

# Define the Email class to map to the emails table in the database
class Email(Base):
    __tablename__ = "emails"

    id = Column(String, primary_key=True)
    From = Column(String, nullable=False)
    Subject = Column(String, nullable=False)
    message = Column(String, nullable=False)
    Date = Column(DateTime, default=datetime.datetime.utcnow)
    label = Column(String, default="inbox")
    To = Column(String, nullable=True)
    Cc = Column(String, nullable=True)

# Change database URL to use PostgreSQL
# DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:Qwik%401234@localhost:5433/email_db")

DATABASE_URL = os.getenv("DATABASE_URL", f"postgresql://{config.get("DatabasesUsername")}:{config.get("DatabasesPassword")}@localhost:{config.get("port")}/{config.get("dbname")}")

# Create database engine
engine = create_engine(DATABASE_URL, echo=True)  # `echo=True` prints SQL queries (useful for debugging)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    """Initialize database tables"""

if __name__ == "__main__":
    init_db() 