from flask import jsonify


def error_response(message, code=400):
    """
    Return structured error JSON response.
    
    Args:
        message (str): Error message
        code (int): HTTP status code
    
    Returns:
        tuple: (jsonify response, http code)
    """
    return jsonify({
        "success": False,
        "error": message,
        "code": code
    }), code


def validation_error(field, message):
    """Return validation error response"""
    return error_response(f"Validation Error - {field}: {message}", 400)


def server_error(message):
    """Return 500 server error response"""
    return error_response(f"Server Error: {message}", 500)
