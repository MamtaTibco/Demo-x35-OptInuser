
# exceptions.py
class ApiException(Exception):
    """
    Exception raised for API-related errors.

    Args:
        message (str): Description of the error.
        error_code (Optional[str|int]): Optional error code for the exception.
        extra (Optional[dict]): Additional context or data for the exception.
    """

    def __init__(self, message, error_code=None, extra=None):
        self.error_code = error_code
        self.extra = get_extra(self.error_code, extra)
        if self.error_code is not None:
            message = f"{self.error_code}: {str(message)}"
        super().__init__(message)


# class PrinterException(Exception):
#     """
#     Exception raised for printer-related errors.
#
#     Args:
#         message (str): Description of the error.
#         error_code (Optional[str|int]): Optional error code for the exception.
#         extra (Optional[dict]): Additional context or data for the exception.
#     """
#
#     def __init__(self, message, error_code=None, extra=None):
#         self.error_code = error_code
#         self.extra = get_extra(self.error_code, extra)
#         if self.error_code is not None:
#             message = f"{self.error_code}: {str(message)}"
#         super().__init__(message)


class DBException(Exception):
    """
    Exception raised for database-related errors.

    Args:
        message (str): Description of the error.
        error_code (Optional[str|int]): Optional error code for the exception.
        extra (Optional[dict]): Additional context or data for the exception.
    """

    def __init__(self, message, error_code=None, extra=None):
        self.error_code = error_code
        self.extra = get_extra(self.error_code, extra)
        if self.error_code is not None:
            message = f"{self.error_code}: {str(message)}"
        super().__init__(message)


# class StoreMislException(Exception):
#     """
#     Exception raised for store mislabeling errors.
#
#     Args:
#         message (str): Description of the error.
#         error_code (Optional[str|int]): Optional error code for the exception.
#         extra (Optional[dict]): Additional context or data for the exception.
#     """
#
#     def __init__(self, message, error_code=None, extra=None):
#         self.error_code = error_code
#         self.extra = get_extra(self.error_code, extra)
#         if self.error_code is not None:
#             message = f"{self.error_code}: {str(message)}"
#         super().__init__(message)


# class ProshipException(Exception):
#     """
#     Exception raised for Proship-related errors.
#
#     Args:
#         message (str): Description of the error.
#         error_code (Optional[str|int]): Optional error code for the exception.
#         extra (Optional[dict]): Additional context or data for the exception.
#     """
#
#     def __init__(self, message, error_code=None, extra=None):
#         self.error_code = error_code
#         self.extra = get_extra(self.error_code, extra)
#         if self.error_code is not None:
#             message = f"{self.error_code}: {str(message)}"
#         super().__init__(message)


# class TransformationException(Exception):
#     """
#     Exception raised for transformation-related errors.
#
#     Args:
#         message (str): Description of the error.
#         error_code (Optional[str|int]): Optional error code for the exception.
#         extra (Optional[dict]): Additional context or data for the exception.
#     """
#
#     def __init__(self, message, error_code=None, extra=None):
#         self.error_code = error_code
#         self.extra = get_extra(self.error_code, extra)
#         if self.error_code is not None:
#             message = f"{self.error_code}: {str(message)}"
#         super().__init__(message)
#
#
# def get_extra(error_code, extra):
#     # Ensure extra is a dictionary
#     if extra is None:
#         extra = {}
#     elif not isinstance(extra, dict):
#         raise TypeError("extra must be a dictionary")
#
#     # Add error_code to extra
#     if error_code is not None:
#         extra["error_code"] = error_code
#     return extra
