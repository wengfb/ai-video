from fastapi import HTTPException, status


class AppException(Exception):
    """应用基础异常"""

    def __init__(self, message: str, code: str = "APP_ERROR"):
        self.message = message
        self.code = code
        super().__init__(message)


class NotFoundError(AppException):
    """资源未找到"""

    def __init__(self, resource: str, id: str):
        super().__init__(
            message=f"{resource} with id '{id}' not found",
            code="NOT_FOUND",
        )


class ValidationError(AppException):
    """验证错误"""

    def __init__(self, message: str):
        super().__init__(message=message, code="VALIDATION_ERROR")


class ExternalServiceError(AppException):
    """外部服务错误"""

    def __init__(self, service: str, message: str):
        super().__init__(
            message=f"{service} error: {message}",
            code="EXTERNAL_SERVICE_ERROR",
        )
