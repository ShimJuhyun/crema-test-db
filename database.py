from sqlmodel import SQLModel, create_engine, Session
from config import settings

DATABASE_URL = f'postgresql://{settings.DB_USER}:{settings.DB_PW}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}'
DEFAULT_MAX_KEY_LENGTH = 128
DEFAULT_MAX_VARCHAR_LENGTH = 256

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_test_user():
    try:
        from auth import hash_password
        from user import User
        # SQLModel.metadata.create_all(engine)
        with Session(engine) as session:
            # Create an test user
            hashed_pw = hash_password("user")
            test_user = User(
                id="user",
                username="tester",
                email="test@test.co.kr",
                hashed_password=hashed_pw,
                ip_address="0.0.0.0"
            )
            session.add(test_user)
            session.commit()
            session.refresh(test_user)
    except Exception as e:
        print("Error creating test user: ", str(e))

def create_chips_sample_data_table(data_file_name: str):
    try:
        from pathlib import Path
        import pandas as pd
        file_name = data_file_name + ".parquet"
        sample_data_path = Path(__file__).resolve().parent.parent / "resources" / file_name
        sample_data_df = pd.read_parquet(sample_data_path)
        sample_data_df.to_sql(data_file_name, engine, if_exists="replace", index=False)
    except Exception as e:
        print("Error creating sample data table: ", str(e))



