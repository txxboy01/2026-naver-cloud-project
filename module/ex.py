# modules/search.py
import os
import pandas as pd

# 프로젝트 루트 기준의 CSV 데이터 경로 설정
CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'papers.csv')

def search_papers_by_keywords(keywords: list, top_k: int = 5) -> pd.DataFrame:
    """
    하이퍼클로바X가 추출한 복수의 키워드 리스트를 활용해 
    data/papers.csv 파일에서 관련 논문을 검색하고 DataFrame으로 반환합니다.
    """
    # 1. 예외 처리: 키워드가 비어있는 경우 빈 데이터프레임 반환
    if not keywords:
        return pd.DataFrame()

    # 2. 예외 처리: 데이터 팀원이 준비한 CSV 파일이 없는 경우
    if not os.path.exists(CSV_PATH):
        print(f"[Error] 논문 DB 파일(CSV)을 찾을 수 없습니다: {CSV_PATH}")
        return pd.DataFrame()
        
    try:
        # 3. CSV 데이터 로드 (인코딩 에러 방지를 위해 utf-8-sig 또는 cp949 고려)
        df = pd.read_csv(CSV_PATH)
        
        # 데이터 정제: 결측치 처리 및 문자열 변환
        # 데이터 팀원의 CSV 컬럼명에 따라 'title', 'content' 또는 'abstract'로 수정될 수 있습니다.
        # 여기서는 기본적으로 title(제목)과 content(내용)로 가정합니다.
        title_col = 'title' if 'title' in df.columns else df.columns[0]
        content_col = 'content' if 'content' in df.columns else df.columns[1]
        
        df[title_col] = df[title_col].fillna('').astype(str)
        df[content_col] = df[content_col].fillna('').astype(str)
        
        # 4. 키워드 매칭 점수 계산 로직
        def calculate_match_score(row):
            score = 0
            text_title = row[title_col].lower()
            text_content = row[content_col].lower()
            
            for keyword in keywords:
                kw = keyword.lower().strip()
                if not kw:
                    continue
                # 가중치: 제목에 키워드가 포함되면 10점, 본문에 포함되면 2점 (시연 퀄리티 UP)
                if kw in text_title:
                    score += 10
                if kw in text_content:
                    score += 2
            return score

        # 5. 모든 논문에 점수 매기기
        df['match_score'] = df.apply(calculate_match_score, axis=1)
        
        # 6. 점수가 0점보다 큰 (매칭된 단어가 있는) 논문만 필터링 후 정렬
        results = df[df['match_score'] > 0].sort_values(by='match_score', ascending=False)
        
        # 7. 상위 k개 결과 반환
        return results.head(top_k)

    except Exception as e:
        print(f"[Error] CSV 검색 중 오류 발생: {e}")
        return pd.DataFrame()

# ==========================================
# 👥 팀원들과 로컬에서 테스트해볼 수 있는 예시 코드
# ==========================================
if __name__ == "__main__":
    # 임의의 키워드로 작동 테스트
    test_keywords = ["챗봇", "하이퍼클로바"]
    print(f"🔎 테스트 키워드: {test_keywords}")
    
    # 함수 실행
    search_results = search_papers_by_keywords(test_keywords, top_k=3)
    print(search_results)
