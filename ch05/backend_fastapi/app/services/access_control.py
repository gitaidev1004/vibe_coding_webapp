"""
ch05/backend_fastapi/app/services/access_control.py
접근제어(Access Control) 서비스.
사용자 확인 -> 역할 확인 -> 권한 확인 -> 기능 실행/접근 차단의 흐름을 구현한다.
"""
from fastapi import HTTPException
from app.repositories.admin_repository import AccessRepository
from app.services.log_service import LogService
from app.models.member import Member


class AccessControlService:
    def __init__(self, access_repository: AccessRepository, log_service: LogService):
        self.access_repository = access_repository
        self.log_service = log_service

    def check_permission(self, member: Member, function_code: str, need_write: bool = False) -> None:
        """
        ① 사용자 확인 -> ② 역할 확인 -> ③ 권한 확인 -> ④ 기능 실행/⑥ 접근 차단
        """
        # ① 사용자 확인: 활성 사용자인지 확인한다.
        if not member.is_active:
            self._deny(member, function_code, "사용 중지된 계정")

        # ② 역할 확인: 사용자에게 역할이 부여되어 있는지 확인한다.
        if member.role is None:
            self._deny(member, function_code, "역할 없음")

        # ③ 권한 확인: 역할이 해당 기능에 대한 권한을 가지고 있는지 확인한다.
        function = self.access_repository.find_function_by_code(function_code)
        if function is None:
            self._deny(member, function_code, "존재하지 않는 기능")

        permission = self.access_repository.find_permission(member.role_id, function.function_id)
        if permission is None:
            self._deny(member, function_code, "권한 없음")

        if need_write and not permission.can_write:
            self._deny(member, function_code, "쓰기 권한 없음")
        if not need_write and not permission.can_read:
            self._deny(member, function_code, "읽기 권한 없음")

        # ④ 기능 실행: 여기까지 통과하면 호출한 쪽에서 실제 기능을 실행한다.
        self.log_service.record(member.member_id, "ACCESS_GRANTED", target=function_code)

    def _deny(self, member: Member, function_code: str, reason: str):
        # ⑥ 접근 차단: 거부 사유를 로그로 남기고 403 오류를 발생시킨다.
        self.log_service.record(member.member_id, "ACCESS_DENIED", target=f"{function_code} ({reason})")
        raise HTTPException(status_code=403, detail=f"접근 권한이 없습니다: {reason}")
