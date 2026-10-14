"""
ch05/backend_flask/app/errors.py
Flask는 예외를 HTTP 응답으로 자동 변환해 주지 않으므로,
공통 예외 클래스를 만들어 라우터에서 일괄적으로 처리한다.
"""


class ApiError(Exception):
    def __init__(self, message, status_code=400):
        self.message = message
        self.status_code = status_code
