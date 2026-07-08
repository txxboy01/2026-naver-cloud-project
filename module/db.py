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
            host=os.getenv("pg-488s3s.vpc-cdb-kr.ntruss.com"),
            port=os.getenv("DB_PORT", "5432"), # 기본값 5432
            database=os.getenv("ncloud-project-001-9dpk"),
            user=os.getenv("userid"),
            password=os.getenv("lab!@1234")
        )
        return conn
    except Exception as e:
        print(f"[Error] DB 연결 실패: {e}")
        return None
