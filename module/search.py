import psycopg2
import os

def search_paper_in_db(keyword):
    # 1. DB 접속 정보 가져오기 (보안을 위해 .env 사용)
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database="내_DB_이름",
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port="5432"
    )
    
    cur = conn.cursor()
    
    # 2. SQL문 작성: 입력한 키워드가 제목이나 내용에 포함된 논문을 찾아라!
    # % 기호는 키워드 앞뒤로 어떤 글자가 와도 상관없다는 뜻입니다.
    query = "SELECT title, content FROM papers WHERE title LIKE %s OR content LIKE %s"
    search_keyword = f"%{keyword}%"
    
    cur.execute(query, (search_keyword, search_keyword))
    
    # 3. 검색 결과 가져오기
    results = cur.fetchall()
    
    # 4. 접속 종료
    cur.close()
    conn.close()
    
    return results