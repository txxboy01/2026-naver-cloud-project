# modules/hcx_api.py
import os
import requests
import json
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

def extract_keywords_from_idea(user_idea: str) -> list:
    """
    사용자가 입력한 일상어 아이디어를 HyperCLOVA X API에 전달하여
    논문 검색에 필요한 전문 기술 키워드 리스트를 추출합니다.
    """
    # 1. 인프라 팀원이 NCP 콘솔에서 발급받아 .env에 적어줄 정보들
    host = os.getenv("HCX_HOST", "https://clovastudio.stream.ntruss.com")
    api_key = os.getenv("HCX_API_KEY")
    gateway_key = os.getenv("HCX_GATEWAY_KEY")
    
    # 예외 처리: API 키가 없는 경우 기본 키워드 예시 반환 (테스트용)
    if not api_key or not gateway_key:
        print("[Warning] API 키가 설정되지 않았습니다. .env 파일을 확인하세요.")
        return ["챗봇", "자연어처리"]  # 임시 반환값

    # 2. HyperCLOVA X에게 내릴 명령(System Prompt)과 사용자 입력 세팅
    # 2일짜리 프로젝트이므로 Few-shot(예시)을 프롬프트에 직접 녹여 효율을 극대화합니다.
    url = f"{host}/testapp/v1/chat-completions/HCX-003" # 혹은 팀에서 지정한 모델 버전
    
    headers = {
        "X-NCP-CLOVASTUDIO-API-KEY": api_key,
        "X-NCP-APIGW-API-KEY": gateway_key,
        "Content-Type": "application/json"
    }
    
    system_message = (
        "당신은 기술 아이디어에서 논문 검색에 가장 적합한 '전문 기술 키워드'를 추출하는 AI입니다. "
        "사용자가 일상어로 아이디어를 말하면, 핵심 기술 단어 2~3개를 콤마(,)로 구분된 파이썬 리스트 형태의 문자열로만 응답하세요. "
        "예시: ['LLM', 'RAG', '임베딩']"
    )
    
    payload = {
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"다음 아이디어에서 논문 검색용 키워드를 추출해줘: {user_idea}"}
        ],
        "temperature": 0.1, # 일관된 키워드 추출을 위해 낮은 온도로 설정
        "maxTokens": 50
    }
    
    try:
        # 3. NCP API 호출
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            # AI가 답변한 텍스트 가져오기 (예: "['챗봇', '인공지능']")
            ai_response_text = result['result']['message']['content'].strip()
            
            # 문자열 형태의 리스트를 실제 파이썬 리스트로 안전하게 변환
            # 만약 AI가 단순 텍스트로 주었을 때를 대비해 예외 처리 포함
            if "[" in ai_response_text and "]" in ai_response_text:
                # 간단한 파싱 또는 json.loads 대용 안전한 변환
                keywords = eval(ai_response_text) 
                if isinstance(keywords, list):
                    return [kw.strip() for kw in keywords]
            
            # 리스트 형태가 아닐 경우 콤마 분할 예외 처리
            return [kw.strip() for kw in ai_response_text.replace("[", "").replace("]", "").replace("'", "").split(",")]
            
        else:
            print(f"[API Error] 상태 코드: {response.status_code}, 메시지: {response.text}")
            return []
            
    except Exception as e:
        print(f"[Error] HyperCLOVA X 호출 중 오류 발생: {e}")
        return []

# ==========================================
# 👥 개발 팀원 1번 파트 로컬 단독 테스트용
# ==========================================
if __name__ == "__main__":
    test_idea = "사람들이 일상어로 질문하면 AI가 똑똑하게 알아듣고 관련된 논문을 자동으로 찾아주는 웹 서비스를 만들고 싶어."
    print(f"💡 입력 아이디어: {test_idea}")
    
    extracted = extract_keywords_from_idea(test_idea)
    print(f"🚀 추출된 키워드 결과: {extracted}")
