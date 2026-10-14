"""
ch05/backend_fastapi/app/services/log_service.py
사용자 활동 이력을 기록하는 서비스. 로그인, 기능 실행, 접근 거부 로그를 남긴다.
"""
from app.repositories.log_repository import LogRepository
from app.models.log import Log


class LogService:
    def __init__(self, repository: LogRepository):
        self.repository = repository

    def record(self, member_id: int | None, action: str, target: str | None = None) -> Log:
        log = Log(member_id=member_id, action=action, target=target)
        return self.repository.save(log)

    def get_recent_logs(self, limit: int = 100):
        return self.repository.find_all(limit)
