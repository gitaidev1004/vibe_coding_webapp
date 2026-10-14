"""
ch05/backend_flask/app/services/log_service.py
사용자 활동 이력을 기록하는 서비스.
"""
from app.models.log import Log


class LogService:
    def __init__(self, repository):
        self.repository = repository

    def record(self, member_id, action, target=None):
        log = Log(member_id=member_id, action=action, target=target)
        return self.repository.save(log)

    def get_recent_logs(self, limit=100):
        return self.repository.find_all(limit)
