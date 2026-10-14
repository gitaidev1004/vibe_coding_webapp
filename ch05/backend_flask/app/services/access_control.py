"""
ch05/backend_flask/app/services/access_control.py
접근제어(Access Control) 서비스.
사용자 확인 -> 역할 확인 -> 권한 확인 -> 기능 실행/접근 차단의 흐름을 구현한다.
"""
from app.errors import ApiError


class AccessControlService:
    def __init__(self, access_repository, log_service):
        self.access_repository = access_repository
        self.log_service = log_service

    def check_permission(self, member, function_code, need_write=False):
        # ① 사용자 확인
        if not member.is_active:
            self._deny(member, function_code, "사용 중지된 계정")

        # ② 역할 확인
        if member.role is None:
            self._deny(member, function_code, "역할 없음")

        # ③ 권한 확인
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

        # ④ 기능 실행 허용
        self.log_service.record(member.member_id, "ACCESS_GRANTED", target=function_code)

    def _deny(self, member, function_code, reason):
        # ⑥ 접근 차단
        self.log_service.record(member.member_id, "ACCESS_DENIED", target=f"{function_code} ({reason})")
        raise ApiError(f"접근 권한이 없습니다: {reason}", 403)
