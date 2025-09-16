from database import create_db_and_tables, create_test_user
import os
import pandas as pd
from sqlalchemy import create_engine, text
from config import settings
import json

from database import create_db_and_tables, create_test_user, create_chips_sample_data_table
from refresh_token import RefreshToken
from chat import Chat
from user import User
from report import ReportArchive

# Postgres 타입 매핑 함수
def map_type(dtype):
    if dtype == 'DATE':
        return 'DATE'
    elif dtype == 'INT64':
        return 'BIGINT'
    elif dtype == 'FLOAT64':
        return 'DOUBLE PRECISION'
    else:
        return 'TEXT'  # string 일단 길이 지정 pass
    
def create_data_table(table_name, data_df, layout_df):
    print(f'★★★★ Create {table_name} ★★★★★')

    # CREATE TABLE 시작
    sql_lines = [f'CREATE TABLE {table_name} (']

    # 컬럼별 생성
    for idx, row in layout_df.iterrows():
        colname = row['항목명'].lower()
        pg_type = map_type(row['type'])
        sql_lines.append(f'    {colname} {pg_type},')

    # 마지막 콤마 제거 + 닫기
    sql_lines[-1] = sql_lines[-1].rstrip(',')  # 마지막 줄 콤마 제거
    sql_lines.append(');')

    # 출력
    print('===== create table sql')
    create_table_sql = '\n'.join(sql_lines)
    print(create_table_sql)

    # insert
    print('===== create empty table')
    db_url = f'postgresql://{settings.DB_USER}:{settings.DB_PW}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}'
    print(db_url)
    engine = create_engine(db_url)

    with engine.connect() as conn:
        conn.execute(text(create_table_sql))

    # insert
    print('★★★★ insert data ★★★★★')
    data_df.columns = data_df.columns.str.lower()

    db_url = f'postgresql://{settings.DB_USER}:{settings.DB_PW}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}'

    engine = create_engine(db_url)

    data_df.to_sql(
        name=table_name,
        con=engine,
        if_exists='append',  # append = INSERT, replace = DROP+CREATE
        index=False
    )

    print('===== confirm data')
    engine = create_engine(db_url)

    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT * FROM {table_name} LIMIT 10;"))
        for row in result:
            print(row)

    print('★★★★ Complete ★★★★★')

if __name__ == '__main__':

    print('★★★★★ Create DB ★★★★★')
    create_db_and_tables()

    print('★★★★★ Create User ★★★★★')
    create_test_user()

    layout_file_path = r"C:\github\crema-test-db\mount\raw_data\structured_report_data_schema_v001.csv"
    layout_df = pd.read_csv(layout_file_path, encoding="cp949")
    
    data_file_path = r"C:\github\crema-test-db\mount\raw_data\structured_report_data_v001.csv"
    data_df = pd.read_csv(data_file_path)
    data_df['RCV_DT'] = pd.to_datetime(data_df['RCV_DT'].astype(str) + '01', format='%Y%m%d')

    create_data_table('df_chips', data_df, layout_df)

    layout_df = pd.read_parquet(r"C:\github\crema-test-db\mount\raw_data\chips_sample_202503_schema.parquet").rename(columns={'feature': '항목명', 'dtype': 'type'})
    data_df = pd.read_parquet(r"C:\github\crema-test-db\mount\raw_data\chips_sample_202503.parquet")
    
    create_data_table('chips_sample_202503', data_df, layout_df)
