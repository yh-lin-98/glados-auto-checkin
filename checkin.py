import os
import sys
import requests

BASE_URL = "https://glados.cloud"

cookie = os.environ.get("GLADOS_COOKIE", "").strip()
user_agent = os.environ.get(
    "GLADOS_USER_AGENT",
    "Mozilla/5.0"
)

if not cookie:
    print("❌ 未配置 GLADOS_COOKIE")
    sys.exit(1)

headers = {
    "Cookie": cookie,
    "User-Agent": user_agent,
    "Content-Type": "application/json",
    "Origin": BASE_URL,
    "Referer": BASE_URL + "/console/checkin"
}

try:
    response = requests.post(
        BASE_URL + "/api/user/checkin",
        headers=headers,
        json={"token": "glados.cloud"},
        timeout=20
    )

    response.raise_for_status()
    result = response.json()

    message = str(result.get("message", ""))
    print("签到结果：", message)

    if (
        "Checkin!" in message
        or "Repeats!" in message
        or result.get("code") == 0
    ):
        print("✅ 签到成功或今日已签到")
    else:
        print("❌ 签到失败")
        sys.exit(1)

except Exception as e:
    print("❌ 请求异常：", str(e))
    sys.exit(1)
