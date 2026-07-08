# app.py
from module.hcx_api import extract_keywords_from_idea # 우리가 만든 비서 호출
from module.search import calculate_match_score # 점수 계산 로직
import pandas as pd
from sqlalchemy import create_engine  # 이 코드가 있어야 DB랑 대화할 수 있는 도구를 가져옵니다.python app.py

def main():
    # 1. 사용자로부터 아이디어 받기
    user_idea = input("구현하고 싶은 기술 아이디어를 입력하세요: ")

    # 2. 하이퍼클로바X에게 키워드 추출 요청
    print("\n[AI가 키워드를 분석 중입니다...]")
    keywords = extract_keywords_from_idea(user_idea)
    print(f"추출된 키워드: {keywords}")

    # 3. 데이터 로드 (DB 방식)
    # 인프라 팀이 준 DB 접속 주소 그대로 사용
    engine = create_engine('postgresql://userid:lab!@1234@pg-488s3s.vpc-cdb-kr.ntruss.com:5432/ncloud-project-001-9dpk')
    df = pd.read_sql('SELECT * FROM papers', engine)

    # 4. 각 논문마다 점수 매기기
    print("[논문을 검색 중입니다...]")
    df['score'] = df.apply(lambda row: calculate_match_score(row, keywords), axis=1)

    # 5. 점수 높은 순으로 정렬해서 상위 3개 보여주기
    result = df.sort_values(by='score', ascending=False).head(3)

    print("\n--- 추천 논문 결과 ---")
    for index, row in result.iterrows():
        print(f"제목: {row['title']} (점수: {row['score']})")

if __name__ == "__main__":
    main()