import os
# Get the environment
env = os.getenv("ENV", "local")

# Set the default DATABASE_URL if not provided
if env == "docker":
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:secret@ktb-database:5432/ktb-scrape")
elif env == "local":
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:secret@ktb-localhost:5432/ktb-scrape")
#elif env == "prod":
#    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:secret@proddb:5432/ktb-scrape")
else:
    DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise Exception("DATABASE_URL not found in environment")