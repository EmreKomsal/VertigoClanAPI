from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Database configuration
# You can set the DATABASE_URL environment variable to your database connection string
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:<your-password>@/cloudsql/vertigo-clan-api:europe-west10:clan-db/clandb")


# Create the SQLAlchemy engine and session
engine = create_engine(DATABASE_URL)
# Create a configured "Session" class
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Create a base class for declarative models
Base = declarative_base()