#!/bin/bash
# ch06/05_deployment/git_workflow_demo.sh
# Repository, Commit, Branch, Merge로 이어지는 기본적인 Git 워크플로를
# 실제 명령으로 실행해 보는 예제 스크립트입니다.
set -e

rm -rf /tmp/git_demo && mkdir -p /tmp/git_demo && cd /tmp/git_demo

echo "=== 1. Repository 초기화 ==="
git init -q
git config user.email "demo@example.com"
git config user.name "Demo User"

echo "=== 2. 첫 Commit ==="
echo "# 실습 프로젝트" > README.md
git add README.md
git commit -q -m "docs: 프로젝트 초기 README 작성"
git log --oneline

echo ""
echo "=== 3. Branch 생성 및 전환 (기능 개발용) ==="
git switch -c feature/comment
echo "댓글 기능 작업 중..." > comment_feature.txt
git add comment_feature.txt
git commit -q -m "feat: 댓글 기능 추가"
git log --oneline --all --graph

echo ""
echo "=== 4. main 브랜치로 돌아가 Merge ==="
git switch main -q 2>/dev/null || git switch master -q
git merge feature/comment -q -m "merge: 댓글 기능 병합"
git log --oneline --all --graph

echo ""
echo "=== 완료: 최종 파일 목록 ==="
ls -1
