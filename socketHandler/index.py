from io_blueprint import IOBlueprint
from flask_socketio import send, emit
socketio = IOBlueprint("/socket")


@socketio.on('connect')
def handle_connect():
    pass


@socketio.on('update-trash')
def update_trash():
    pass
