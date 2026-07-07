import psycopg2
import os
from dotenv import load_dotenv

# .env 파일 불러오기
load_dotenv()

def get_db_connection():
    """
    환경 변수에서 DB 접속 정보를 가져와 연결 객체를 반환합니다.
    """
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT", "5432"), # 기본값 5432
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        return conn
    except Exception as e:
        print(f"[Error] DB 연결 실패: {e}")
        return None
