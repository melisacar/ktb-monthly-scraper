from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Database connection
#database_url = 'postgresql+psycopg2://postgres:secret@database:5432/ktb-scrape'
DATABASE_URL = 'postgresql+psycopg2://postgres:secret@localhost:5432/ktb-scrape'

# Create the engine
engine = create_engine(DATABASE_URL)

# Create a session for database operations.
Session = sessionmaker(bind=engine)