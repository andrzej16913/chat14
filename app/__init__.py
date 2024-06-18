from flask import Flask
from config import Config
from flask_login import LoginManager
from flask_bootstrap import Bootstrap5
from flask_socketio import SocketIO
from mongoengine import connect

app = Flask(__name__)
app.config.from_object(Config)
connect('chat14')
bootstrap = Bootstrap5(app)
lm = LoginManager(app)
lm.login_view = 'login'
socketio = SocketIO(app)

from app.models import Room

app.app_context().push()
rooms = set()
for room in Room.objects:
    print(room.name)
    rooms.add(room)
    room.namespace = room.name
    socketio.on_namespace(room)

from app import routes
