"""Custom errors so callers can react to *why* something failed."""


class EcomError(Exception):
    """Base error for this package."""


class DataIngestionError(EcomError):
    """Raised when the raw data cannot be read."""


class DataValidationError(EcomError):
    """Raised when data breaks the agreed schema or quality rules."""


class ModelNotReadyError(EcomError):
    """Raised when inference is attempted without a usable model."""
