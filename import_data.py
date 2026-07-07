import pandas as pd
import psycopg2
import os

# 1. CSV 파일 읽기
df = pd.read_csv('data/paper.csv')

# 2. DB 접속
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database="내_DB_이름",
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port="5432"
)
cur = conn.cursor()

# 3. 데이터 한 줄씩 DB에 넣기
for index, row in df.iterrows():
    # 'papers'라는 테이블에 제목과 내용을 넣습니다.
    sql = "INSERT INTO papers (title, content) VALUES (%s, %s)"
    cur.execute(sql, (row['title'], row['content']))

# 4. 저장하고 끝내기
conn.commit()
cur.close()
conn.close()

print("데이터 입력 완료!")
