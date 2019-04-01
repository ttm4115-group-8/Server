import eventlet
from flask import Flask, render_template, render_template_string
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
#from users import User
from flask_user import login_required, UserManager, UserMixin


eventlet.monkey_patch()


app = Flask(__name__, template_folder='./views')
app.config['MQTT_BROKER_URL'] = '129.241.208.68'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_REFRESH_TIME'] = 1.0
app.config['USER_ENABLE_EMAIL'] = False
app.config['USER_ENABLE_USERNAME'] = True
app.config['USER_REQUIRE_RETYPE_PASSWORD'] = False
app.config['SECRET_KEY'] = 'This is an INSECURE secret!! DO NOT use this in production!!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quickstart_app.sqlite'    # File-based SQL database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Avoids SQLAlchemy warning

mqtt = Mqtt(app)
socketio = SocketIO(app)

### DB setup ###
 # Initialize Flask-SQLAlchemy
db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')

    username = db.Column(db.String(100, collation='NOCASE'), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    email_confirmed_at = db.Column(db.DateTime())

    #User information
    first_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')
    last_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')

# Create all database tables
db.create_all()
# Setup Flask-User and specify the User data-model
user_manager = UserManager(app, db, User)

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('#')


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    # emit a mqtt_message event to the socket containing the message data
    socketio.emit('mqtt_message', data=data)


@app.route('/')
def home_page():
    # String-based templates
    return render_template_string("""
        {% extends "flask_user_layout.html" %}
        {% block content %}
            <h2>Home page</h2>
            <p><a href={{ url_for('user.register') }}>Register</a></p>
            <p><a href={{ url_for('user.login') }}>Sign in</a></p>
            <p><a href={{ url_for('home_page') }}>Home page</a> (accessible to anyone)</p>
            <p><a href={{ url_for('member_page') }}>Member page</a> (login required)</p>
            <p><a href={{ url_for('graph') }}>view graph</a> (login required)</p>
            <p><a href={{ url_for('user.logout') }}>Sign out</a></p>
        {% endblock %}
        """)

@app.route('/members')
@login_required
def member_page():
    # String-based templates
    return render_template_string("""
        {% extends "flask_user_layout.html" %}
        {% block content %}
            <h2>Members page</h2>
            <p><a href={{ url_for('user.register') }}>Register</a></p>
            <p><a href={{ url_for('user.login') }}>Sign in</a></p>
            <p><a href={{ url_for('home_page') }}>Home page</a> (accessible to anyone)</p>
            <p><a href={{ url_for('member_page') }}>Member page</a> (login required)</p>
            <p><a href={{ url_for('graph') }}>view graph</a> (login required)</p>
            <p><a href={{ url_for('user.logout') }}>Sign out</a></p>

        {% endblock %}
        """)

@app.route('/graph')
@login_required
def graph():
    return render_template('graph.html')


@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    print(level, buf)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8000)
    
