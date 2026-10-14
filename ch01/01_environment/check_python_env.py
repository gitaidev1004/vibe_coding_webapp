"""
ch01/01_environment/check_python_env.py
Python 개발 환경(FastAPI, Flask 실습용) 확인 스크립트
"""
import sys
import platform


def check_python_version():
    major, minor = sys.version_info.major, sys.version_info.minor
    print(f"Python 버전   : {platform.python_version()}")
    if (major, minor) >= (3, 10):
        print(" -> FastAPI / Flask 실습에 적합한 버전입니다.")
    else:
        print(" -> Python 3.10 이상 버전 사용을 권장합니다.")


def check_package(package_name):
    try:
        __import__(package_name)
        print(f"{package_name:10s} : 설치되어 있습니다.")
    except ImportError:
        print(f"{package_name:10s} : 설치되어 있지 않습니다. (pip install {package_name})")


if __name__ == "__main__":
    print("=== Python 개발 환경 점검 ===")
    check_python_version()
    print()
    print("=== 주요 패키지 설치 확인 ===")
    for pkg in ["fastapi", "flask", "sqlalchemy"]:
        check_package(pkg)
