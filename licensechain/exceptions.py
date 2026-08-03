"""
LicenseChain Python SDK Exceptions

Custom exceptions for the LicenseChain Python SDK.
"""


class LicenseChainException(Exception):
    """Base exception for all LicenseChain errors."""

    def __init__(self, message: str = "LicenseChain error occurred", *args, **kwargs):
        super().__init__(message, *args, **kwargs)
        self.message = message


class AuthenticationError(LicenseChainException):
    """Exception raised when authentication fails."""

    def __init__(self, message: str = "Authentication failed", *args, **kwargs):
        super().__init__(message, *args, **kwargs)


class ValidationError(LicenseChainException):
    """Exception raised when request validation fails."""

    def __init__(self, message: str = "Validation failed", *args, **kwargs):
        super().__init__(message, *args, **kwargs)


class NotFoundError(LicenseChainException):
    """Exception raised when a resource is not found."""

    def __init__(self, message: str = "Resource not found", *args, **kwargs):
        super().__init__(message, *args, **kwargs)


class RateLimitError(LicenseChainException):
    """Exception raised when rate limit is exceeded."""

    def __init__(self, message: str = "Rate limit exceeded", *args, **kwargs):
        super().__init__(message, *args, **kwargs)


class ServerError(LicenseChainException):
    """Exception raised when server returns an error."""

    def __init__(self, message: str = "Server error", *args, **kwargs):
        super().__init__(message, *args, **kwargs)


class NetworkError(LicenseChainException):
    """Exception raised when network operations fail."""

    def __init__(self, message: str = "Network error", *args, **kwargs):
        super().__init__(message, *args, **kwargs)


class ApiError(LicenseChainException):
    """Exception raised for API-related errors."""

    def __init__(self, message: str = "API error", *args, **kwargs):
        super().__init__(message, *args, **kwargs)


class TimeoutError(LicenseChainException):
    """Exception raised when a request times out."""

    def __init__(self, message: str = "Request timeout", *args, **kwargs):
        super().__init__(message, *args, **kwargs)


class SerializationError(LicenseChainException):
    """Exception raised when serialization fails."""

    def __init__(self, message: str = "Serialization failed", *args, **kwargs):
        super().__init__(message, *args, **kwargs)


class DeserializationError(LicenseChainException):
    """Exception raised when deserialization fails."""

    def __init__(self, message: str = "Deserialization failed", *args, **kwargs):
        super().__init__(message, *args, **kwargs)


class ConfigurationError(LicenseChainException):
    """Exception raised when configuration is invalid."""

    def __init__(self, message: str = "Configuration error", *args, **kwargs):
        super().__init__(message, *args, **kwargs)


class UnknownError(LicenseChainException):
    """Exception raised for unknown errors."""

    def __init__(self, message: str = "Unknown error", *args, **kwargs):
        super().__init__(message, *args, **kwargs)


# Aliases for backward compatibility
LicenseChainError = LicenseChainException
