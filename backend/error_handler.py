from flask import jsonify


def error_response(message, code=400, request_id=None):
    """
    Return structured error JSON response with optional request ID for tracing.
    
    Args:
        message (str): Error message
        code (int): HTTP status code
        request_id (str): Optional correlation ID for debugging
    
    Returns:
        tuple: (jsonify response, http code)
    """
    response = {
        "success": False,
        "error": message,
        "code": code
    }
    
    if request_id:
        response["request_id"] = request_id
    
    return jsonify(response), code


def validation_error(field, message, request_id=None):
    """Return validation error response with optional request ID"""
    return error_response(f"Validation Error - {field}: {message}", 400, request_id)


def server_error(message, request_id=None):
    """Return 500 server error response with optional request ID"""
    return error_response(f"Server Error: {message}", 500, request_id)
