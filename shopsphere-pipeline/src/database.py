from sqlalchemy import create_engine


DATABASE_URL = (
    "postgresql+psycopg2://postgres:"
    "@localhost:5432/shopsphere"
)


def get_engine():
    return create_engine(DATABASE_URL)