from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def index(request):
    print(request.method)
    return render(request, "one.html")

import requests
@csrf_exempt
def billings(request):
    billingKey= ""
    # print(request.method)
    # 고객사에서 채번하는 새로운 결제 ID를 만듭니다.
    payment_id = 1234 # 이 부분은 해당 함수의 Python 구현에 따라 다를 수 있습니다.

    # 포트원 빌링키 결제 API 호출
    url = f"https://api.portone.io/payments/{}/billing-key"
    headers = {
        "Authorization": f"PortOne ",
        "Content-Type": "application/json",
    }

    # 고객 정보와 요청 바디 구성
    data = {
        "billingKey": billingKey,
        "orderName": "월간 이용권 정기결제",
        "customer": {
            "id": "hans",
    },  # 실제 고객 정보로 채워야 합니다.
        "amount": {
            "total": 8900,
        },
        "currency": "KRW",
    }

    response = requests.post(url, headers=headers, json=data)

    # 응답 상태 검사
    if not response.ok:
        raise Exception(f"paymentResponse: {response.status_code} {response.text}")

    # 응답 데이터 출력 또는 추가 처리
    print(response.json())
    return render(request, "index.html")