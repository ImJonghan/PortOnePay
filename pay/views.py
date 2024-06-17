from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os
import dotenv

""" .env file
storeId=
channelKey=
billing_key=
PORTONE_API_KEY= #portone v2 api key
"""
dotenv.load_dotenv()
# Create your views here.
@csrf_exempt
def index(request):
    print(request.method)
    storeId=os.getenv("storeId")
    channelKey=os.getenv("channelKey")
    context={
        "storeId":storeId,
        "channelKey":channelKey
    }
    return render(request, "one.html",context)

import requests
import urllib.parse

@csrf_exempt
def billings(request):
    # 실제 로직은 위에서 billingkey를 발급받고 DB에 저장
    # 경매가 완료되면 아래 프로세스 실행되도록 하면 되겠습니다!

    billing_key=os.getenv("billing_key")
    PORTONE_API_KEY=os.getenv("PORTONE_API_KEY")
    # print(request.method)
    # 고객사에서 채번하는 새로운 결제 ID를 만듭니다.
    payment_id = "test1234" # 이 부분은 해당 함수의 Python 구현에 따라 다를 수 있습니다.
    encoded_payment_id = urllib.parse.quote(payment_id)
    # 포트원 빌링키 결제 API 호출
    url = f"https://api.portone.io/payments/{encoded_payment_id}/billing-key"
    headers = {
        "Authorization": f"PortOne {PORTONE_API_KEY}",
        "Content-Type": "application/json",
    }

    # 고객 정보와 요청 바디 구성
    data = {
        "billingKey": billing_key,
        "orderName": "월간 이용권 정기결제",
        "customer": {
            "id": "hans",
    },  # 실제 고객 정보로 채워야 합니다.
        "amount": {
            "total": 8900,
        },
        "currency": "KRW",
    }
    # v2의 API 키 발급 따로 받아야 함
    # '{"type":"INVALID_REQUEST","message":"Invalid value for: body\\nexpected \'\\"\', offset: 0x0000000f, buf:\\n+----------+-------------------------------------------------+------------------+\\n|          |  0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f | 0123456789abcdef |\\n+----------+-------------------------------------------------+------------------+\\n| 00000000 | 7b 22 62 69 6c 6c 69 6e 67 4b 65 79 22 3a 20 6e | {\\"billingKey\\": n |\\n| 00000010 | 75 6c 6c 2c 20 22 6f 72 64 65 72 4e 61 6d 65 22 | ull, \\"orderName\\" |\\n| 00000020 | 3a 20 22 5c 75 63 36 64 34 5c 75 61 63 30 34 20 | : \\"\\\\uc6d4\\\\uac04  |\\n+----------+-------------------------------------------------+------------------+\\nThe original input: {\\"billingKey\\": null, \\"orderName\\": \\"\\\\uc6d4\\\\uac04 \\\\uc774\\\\uc6a9\\\\uad8c \\\\uc815\\\\uae30\\\\uacb0\\\\uc81c\\", \\"customer\\": {\\"id\\": \\"hans\\"}, \\"amount\\": {\\"total\\": 8900}, \\"currency\\": \\"KRW\\"}"}'

    response = requests.post(url, headers=headers, json=data)

    # 응답 상태 검사
    if not response.ok:
        raise Exception(f"paymentResponse: {response.status_code} {response.text}")

    # 응답 데이터 출력 또는 추가 처리
    print(response.json())
    return render(request, "index.html")