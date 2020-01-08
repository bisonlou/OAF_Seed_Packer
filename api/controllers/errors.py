from api import app
from flask import abort, jsonify

@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
        'success': False,
        'message': 'resource not found',
        'error': 404
    }), 404


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'message': 'bad request',
        'error': 400
    }), 400

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        'success': False,
        'message': 'unauthorized',
        'error': 401
    }), 401

@app.errorhandler(403)
def permission_denied(error):
    return jsonify({
        'success': False,
        'message': 'permission denied',
        'error': 403
    }), 403

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'success': False,
        'message': 'method not allowed',
        'error': 405
    }), 405