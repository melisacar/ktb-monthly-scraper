from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Database connection
database_url = 'postgresql://postgres:secret@database:5432/ktb-scrape'

# Create the engine
engine = create_engine(database_url)

# Create a session for database operations.
Session = sessionmaker(bind=engine)