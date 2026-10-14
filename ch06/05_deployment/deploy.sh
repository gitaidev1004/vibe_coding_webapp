#!/bin/bash
# ch06/05_deployment/deploy.sh
# 프런트엔드 빌드 -> 백엔드 빌드 -> 컨테이너 기동까지 이어지는
# 배포 절차를 하나로 정리한 예제 스크립트입니다.
set -e

echo "=== 1. Vue 프런트엔드 빌드 ==="
(cd ch04/vue_project && npm install && npm run build)

echo "=== 2. FastAPI 백엔드 의존성 확인 ==="
(cd ch05/backend_fastapi && pip install -r requirements.txt)

echo "=== 3. 전체 테스트 실행 (배포 전 최종 검증) ==="
(cd ch05/backend_fastapi && python -m pytest tests/ -q)

echo "=== 4. Docker 이미지 빌드 및 컨테이너 기동 ==="
docker compose -f ch06/05_deployment/docker-compose.yml up -d --build

echo "=== 5. 배포 후 헬스 체크 ==="
sleep 5
python3 ch06/06_operations/health_check.py

echo "=== 배포 완료 ==="
