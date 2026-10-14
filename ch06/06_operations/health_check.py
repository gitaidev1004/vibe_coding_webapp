"""
ch06/06_operations/health_check.py
배포된 백엔드가 정상적으로 응답하는지 주기적으로 확인하는 간단한
모니터링 스크립트 예제입니다. (운영 중 장애를 빠르게 감지하기 위한 용도)
"""
import urllib.request
import urllib.error
import time
import sys

CHECK_TARGETS = [
    {"name": "FastAPI 백엔드", "url": "http://localhost:8000/"},
    {"name": "Flask 백엔드", "url": "http://localhost:5000/"},
]


def check_health(target: dict) -> dict:
    try:
        start = time.time()
        with urllib.request.urlopen(target["url"], timeout=3) as response:
            elapsed_ms = (time.time() - start) * 1000
            return {
                "name": target["name"], "status": "UP",
                "http_status": response.status, "elapsed_ms": round(elapsed_ms, 1),
            }
    except urllib.error.URLError as e:
        return {"name": target["name"], "status": "DOWN", "error": str(e.reason)}


def run_health_checks():
    print(f"=== 헬스 체크 실행 ({time.strftime('%Y-%m-%d %H:%M:%S')}) ===")
    all_up = True
    for target in CHECK_TARGETS:
        result = check_health(target)
        if result["status"] == "UP":
            print(f"  [UP]   {result['name']:15s} {result['http_status']} ({result['elapsed_ms']}ms)")
        else:
            all_up = False
            print(f"  [DOWN] {result['name']:15s} 오류: {result['error']}")
    return all_up


if __name__ == "__main__":
    healthy = run_health_checks()
    sys.exit(0 if healthy else 1)
