from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_name = "boba_data.db"
SQLALCHEMY_DATABASE_URI = "sqlite:///" + db_name

engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)