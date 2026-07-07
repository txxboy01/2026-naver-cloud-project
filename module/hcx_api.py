# 하이퍼 클로바 x API 호출 모듈
import requests
import json

def call_hyperclova(prompt):
    # 1. API 주소와 인증 정보 설정
    api_url = "여기에 네이버에서 받은 API URL을 넣으세요"
    api_key = "내 API Key"
    secret_key = "내 Secret Key"

    # 2. 통신을 위한 약속(헤더) 정하기
    headers = {
        "X-NCP-CLOVAAPI-KEY": api_key,
        "X-NCP-APIGW-API-KEY": secret_key,
        "Content-Type": "application/json; charset=utf-8"
    }

    # 3. AI에게 보낼 메시지 (질문)
    data = {
        "messages": [
            {"role": "system", "content": "너는 똑똑한 비서야."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.5,
        "maxTokens": 500
    }

    # 4. AI에게 요청 보내기
    response = requests.post(api_url, headers=headers, json=data)

    # 5. 결과 받아서 돌려주기
    if response.status_code == 200:
        result = response.json()
        return result['result']['message']['content']
    else:
        return f"에러가 났어! 번호: {response.status_code}"