class WebAPIException(Exception):
    """
    发布 Web API 的异常信息
    """
    def __init__(self, status_code, message, other=""):
        self.status_code = status_code
        self.message = message
        self.other = other

    def __str__(self):
        return f"HTTPException: {self.status_code} - {self.message}:{self.other}"
