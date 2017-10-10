from flask import request, jsonify, abort, Blueprint


def to_json(data, message, code):
     return jsonify({
        'data': data,
        'status_code': code,
        'message': message
    })


