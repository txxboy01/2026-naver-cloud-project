# app.py
from module.hcx_api import call_hyperclova  # 우리가 만든 비서 호출
from module.search import calculate_match_score # 점수 계산 로직
import pandas as pd

def main():
    # 1. 사용자로부터 아이디어 받기
    user_idea = input("구현하고 싶은 기술 아이디어를 입력하세요: ")

    # 2. 하이퍼클로바X에게 키워드 추출 요청
    print("\n[AI가 키워드를 분석 중입니다...]")
    keywords = call_hyperclova(user_idea)
    print(f"추출된 키워드: {keywords}")

    # 3. 데이터 로드 (논문 리스트 불러오기)
    # 실제로는 DB에서 가져오겠지만, 지금은 테스트용 CSV 활용
    df = pd.read_csv('data/paper.csv')

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