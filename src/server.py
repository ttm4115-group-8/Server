import eventlet
from flask import Flask, session, render_template, render_template_string, request, redirect, url_for
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
# from users import User
from flask_user import login_required, UserManager, UserMixin, current_user
from user_form import Form
from flask_wtf import FlaskForm

eventlet.monkey_patch()

app = Flask(__name__, template_folder='./views')
app.config['MQTT_BROKER_URL'] = '129.241.208.68'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_REFRESH_TIME'] = 1.0
app.config['USER_ENABLE_EMAIL'] = False
app.config['USER_ENABLE_USERNAME'] = True
app.config['USER_REQUIRE_RETYPE_PASSWORD'] = False
app.config['SECRET_KEY'] = 'This is an INSECURE secret!! DO NOT use this in production!!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quickstart_app.sqlite'  # File-based SQL database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Avoids SQLAlchemy warning
app.config['USER_APP_NAME'] = "YOUR SLEEP MONITOR"
mqtt = Mqtt(app)
socketio = SocketIO(app)

### DB setup ###
# Initialize Flask-SQLAlchemy
db = SQLAlchemy(app)

# TODO: Add user fields
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')

    username = db.Column(db.String(100, collation='NOCASE'), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    email_confirmed_at = db.Column(db.DateTime())

    # User information
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

    if data['topic'] == "timer_request":
        with open("timer.txt", "r") as file:
            timer_str = file.readline()
            mqtt.publish('timer_response', bytes(timer_str, 'utf-8'))

    # emit a mqtt_message event to the socket containing the message data
    socketio.emit('mqtt_message', data=data)


@app.route('/')
def home_page():
    return render_template('home_page.html', current_user=current_user)


@app.route('/user/<username>')
@login_required
def user_page(username='test'):
    return render_template('user_page.html', username=username)


@app.route('/user/<username>/graph')
@login_required
def graph(username):
    return render_template('graph.html', username=username)

@app.route('/user/<username>/edit_user')
@login_required
def edit_user(username):
    form = Form()
    return render_template('edit_user.html', current_user=current_user, form=form, username=username, wtf=FlaskForm)


@app.route('/user/<username>/sleep_recommendations')
@login_required
def sleep_recommendations(username):
    return render_template('sleep_recommendations.html', username=username)


@app.route('/user/<username>/set_timer')
@login_required
def set_timer(username):
    return render_template('set_timer.html', username=username)


@app.route('/user/<username>/handle_timer_data', methods=['POST'])
@login_required
def handle_timer_data(username):
    with open("timer.txt", "w") as file:
        file.write(request.form['timer'])

    # This is a ugly hack to get out of the redirect loop that happens
    return render_template('home_page.html')


@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    print(level, buf)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8000)
