from typing import Callable, Optional
from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

class UserException(Exception):
    """Base class for user-related errors."""
    pass

class InvalidToken(UserException):
    """User has provided an invalid or expired token."""
    pass

class RevokedToken(UserException):
    """User has provided a token that has been revoked."""
    pass

class AccessTokenRequired(UserException):
    """User has provided a refresh token when an access token is needed."""
    pass

class RefreshTokenRequired(UserException):
    """User has provided an access token when a refresh token is needed."""
    pass

class UserAlreadyExists(UserException):
    """User has provided an email for a user who exists during sign up."""
    pass

class PasswordException(Exception):
    """Base class for password-related errors."""
    pass

class PasswordTooShort(PasswordException):
    """Password does not meet minimum length requirement."""
    pass

class PasswordTooWeak(PasswordException):
    """Password does not meet strength requirements (e.g., missing numbers or symbols)."""
    pass

class PasswordMismatch(PasswordException):
    """Provided passwords do not match (e.g., during password confirmation)."""
    pass

class InvalidCredentials(UserException):
    """User has provided wrong email or password during log in."""
    pass

class InsufficientPermission(UserException):
    """User does not have the necessary permissions to perform an action."""
    pass

class UserNotFound(UserException):
    """User Not found."""
    pass

class AccountNotVerified(UserException):
    """Account not yet verified."""
    pass

def create_exception_handler(
        status_code: int, detail: str, error_code: str, resolution: Optional[str] = None
) -> Callable[[Request, Exception], JSONResponse]:
    """Create an exception handler for specific error details."""
    async def exception_handler(request: Request, exc: Exception):
        response_content = {
            "detail": detail,
            "error_code": error_code,
            **({"resolution": resolution} if resolution else {}),
            "message": str(exc) if exc.args else "An error occurred."
        }
        return JSONResponse(content=response_content, status_code=status_code)

    return exception_handler

def register_all_errors(app: FastAPI) -> None:
    error_definitions = {
        UserAlreadyExists: {
            "status_code": status.HTTP_403_FORBIDDEN,
            "detail": "This email is already associated with an account.",
            "error_code": "user_exists",
            "resolution": "Try logging in or using a different email."
        },
        UserNotFound: {
            "status_code": status.HTTP_404_NOT_FOUND,
            "detail": "We couldn't find a user with the specified details.",
            "error_code": "user_not_found",
        },
        # Password errors
        PasswordTooShort: {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "detail": "Your password is too short.",
            "error_code": "password_too_short",
            "resolution": "Ensure the password meets the minimum length requirements."
        },
        PasswordTooWeak: {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "detail": "Your password does not meet strength requirements.",
            "error_code": "password_too_weak",
            "resolution": "Use a stronger password with numbers, symbols, and uppercase letters."
        },
        PasswordMismatch: {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "detail": "The passwords provided do not match.",
            "error_code": "password_mismatch",
            "resolution": "Ensure both passwords are identical."
        },
        InvalidCredentials: {
            "status_code": status.HTTP_401_UNAUTHORIZED,
            "detail": "Incorrect email or password.",
            "error_code": "invalid_credentials",
            "resolution": "Check your credentials and try again."
        },
        InvalidToken: {
            "status_code": status.HTTP_401_UNAUTHORIZED,
            "detail": "The provided token is invalid or has expired.",
            "error_code": "invalid_token",
            "resolution": "Please request a new token."
        },
        RevokedToken: {
            "status_code": status.HTTP_401_UNAUTHORIZED,
            "detail": "The token provided has been revoked.",
            "error_code": "revoked_token",
            "resolution": "Request a new token to continue."
        },
        AccessTokenRequired: {
            "status_code": status.HTTP_403_FORBIDDEN,
            "detail": "An access token is required for this action.",
            "error_code": "access_token_required",
        },
        RefreshTokenRequired: {
            "status_code": status.HTTP_403_FORBIDDEN,
            "detail": "A refresh token is required for this action.",
            "error_code": "refresh_token_required",
        },
        InsufficientPermission: {
            "status_code": status.HTTP_403_FORBIDDEN,
            "detail": "You lack the necessary permissions to perform this action.",
            "error_code": "insufficient_permissions",
        },
        AccountNotVerified: {
            "status_code": status.HTTP_403_FORBIDDEN,
            "detail": "Your account has not yet been verified.",
            "error_code": "account_not_verified",
            "resolution": "Please check your email for verification instructions."
        },
    }

    for error_class, details in error_definitions.items():
        app.add_exception_handler(
            error_class,
            create_exception_handler(
                status_code=details["status_code"],
                detail=details["detail"],
                error_code=details["error_code"],
                resolution=details.get("resolution"),
            ),
        )

    @app.exception_handler(500)
    async def internal_server_error(request: Request, exc: Exception):
        return JSONResponse(
            content={
                "detail": "An internal server error occurred.",
                "error_code": "server_error",
                "message": str(exc) if exc.args else "Please try again later."
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    @app.exception_handler(SQLAlchemyError)
    async def database_error(request: Request, exc: SQLAlchemyError):
        return JSONResponse(
            content={
                "detail": "A database error occurred while processing your request.",
                "error_code": "database_error",
                "message": str(exc) if exc.args else "Please contact support if the issue persists."
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
