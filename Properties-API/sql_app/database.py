from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = (
    #"mssql+pyodbc://fastapi:fastapi@DESKTOP-I5PBD1V/olp?driver=ODBC+Driver+17+for+SQL+Server"
    "mssql+pyodbc://fuckingshit:sbI2024!@sbi-data-storage.database.windows.net/olp?driver=ODBC+Driver+17+for+SQL+Server"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL,
                       #connect_args={"check_same_thread": False}, ONLY SQL LITE
                        )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()