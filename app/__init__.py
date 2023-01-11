from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap5
from flask_socketio import SocketIO

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap5(app)
lm = LoginManager(app)
lm.login_view = 'login'
socketio = SocketIO(app)

from app.models import Room

app.app_context().push()
rooms = db.session.execute(db.select(Room)).scalars().all()
for room in rooms:
    print(room.name)
    room.namespace = room.name
    socketio.on_namespace(room)

from app import routes
