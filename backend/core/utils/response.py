def success_response(data=None, message=""):
    return {
        "success": True,
        "data": data,
        "message": message
    }


def error_response(message="", errors=None):
    return {
        "success": False,
        "message": message,
        "errors": errors or {}
    }