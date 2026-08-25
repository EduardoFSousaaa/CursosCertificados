class AppError(Exception):
    status_code: int = 500
    message: str = "An unexpected error occurred."

    def __init__(self, message: str | None = None):
        super().__init__(message or self.message)
        if message:
            self.message = message


class NotFoundError(AppError):
    status_code = 404
    message = "Resource not found."


class UnauthorizedError(AppError):
    status_code = 401
    message = "Authentication required."


class ForbiddenError(AppError):
    status_code = 403
    message = "You do not have permission to perform this action."


class ValidationError(AppError):
    status_code = 422
    message = "Validation failed."
