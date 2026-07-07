
import requests
import json
import os
import uuid  # 요청마다 고유 ID를 만들기 위해 필요
from dotenv import load_dotenv

# .env 파일 로드 (최상위 폴더에 있어야 합니다)
load_dotenv()

def call_hyperclova(prompt):
    """
    하이퍼클로바X API를 호출하여 답변을 받아오는 함수
    """
    # .env에서 설정값 불러오기
    api_url = os.getenv("CLOVA_API_URL")
    api_key = os.getenv("CLOVA_API_KEY")
    secret_key = os.getenv("SECRET_KEY")

    # 헤더 설정
    headers = {
        "X-NCP-CLOVAAPI-KEY": api_key,
        "X-NCP-APIGW-API-KEY": secret_key,
        "X-NCP-CLOVAAPI-REQUEST-ID": str(uuid.uuid4()), # 매번 새로운 고유 ID 생성
        "Content-Type": "application/json; charset=utf-8"
    }

    # 대화 데이터 설정
    data = {
        "messages": [
            {"role": "system", "content": "너는 기술 논문을 분석하는 전문 비서야."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.5,
        "maxTokens": 500
    }

    try:
        # API 호출
        response = requests.post(api_url, headers=headers, json=json.dumps(data))
        
        # 결과 확인
        if response.status_code == 200:
            result = response.json()
            return result['result']['message']['content']
        else:
            return f"에러 발생! 상태 코드: {response.status_code}, 상세 내용: {response.text}"
            
    except Exception as e:
        return f"통신 중 오류가 발생했습니다: {str(e)}"