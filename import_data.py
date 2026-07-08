import pandas as pd
from sqlalchemy import create_engine
import os

# 1. 데이터 불러오기 (data 폴더 안에 있다면 경로 주의!)
# 만약 paper.csv가 data 폴더 안에 있다면 'data/paper.csv'로 수정하세요.
df = pd.read_csv('data/paper.csv')

# 2. DB 연결 정보 설정
# 인프라 담당자에게 받은 정보를 입력합니다.
DB_URL = "postgresql://유저명:비밀번호@호스트주소:5432/DB명"
engine = create_engine(DB_URL)

# 3. CSV를 DB로 전송
# if_exists='replace'는 테이블이 이미 있으면 지우고 새로 만든다는 뜻입니다.
df.to_sql('papers', engine, if_exists='replace', index=False)

print("데이터 전송 완료!")
