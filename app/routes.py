import json

from werkzeug.security import check_password_hash
from datetime import timedelta
from . import app
from datetime import datetime
import requests
from flask import render_template, request, redirect, jsonify, make_response
from flask_login import current_user, login_user, login_required, logout_user, login_manager
from .forms import LoginForm, SignupForm
from .db_controls import get_events_by, add_new_item
from .database import Event, User, session
from flask_jwt_extended import create_access_token

# from app import login_manager


def convert_time_to_object(time):
    return datetime.strptime(time, "%H:%M").time()


def convert_date_to_object(date):
    return datetime.strptime(date, "%Y-%m-%d").date()


def add_event_to_database(event_data):
    event_data["time"] = convert_time_to_object(event_data["time"])
    event_data["date"] = convert_date_to_object(event_data["date"])
    event_data["user"] = 1
    event = Event(**event_data)
    add_new_item(event)


def commit_new_item(item):
    session.add(item)
    session.commit()
    session.close()

def create_response(status_code):
    response = make_response()
    response.status_code = status_code
    return response


@app.route("/create_event", methods=["POST"])
def create_event():
    data_from_request = request.get_json()
    print(data_from_request)
    try:
        add_event_to_database(data_from_request)
        response = create_response(200)
    except Exception as e:
        print(e)
        response = create_response(500)

    return response
@app.route("/get_events_by_date/<date>", methods=["GET"])
def get_events_by_date(date):
    print(date)
    date = datetime.fromisoformat(date)
    get_events_by(date)
    response = make_response(data)
    return response




@app.route("/")
@app.route("/main")
def index():
    return render_template("main.html")


@app.route("/login", methods=["POST"])
def login():
    data_from_request = request.get_json()

    name = data_from_request["nickname"]
    password = data_from_request["password"]

    user_check = session.query(User).where(User.nickname == name).first()

    if not user_check:
        print(name, password)
        response = make_response({"isLogged": False})
        return response

    if check_password_hash(user_check.password, password):
        print(name, password)
        token = create_access_token(identity=user_check.id, expires_delta=timedelta(days=30))
        response = make_response({"isLogged": True, "token": token})
        return response

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if request.method == "POST":
        name = form.nickname.data
        password = form.password.data
        email = form.email.data
        new_user = User(str(name), str(password), str(email))

        commit_new_item(new_user)
        return render_template("main.html", message="Done!")

    return render_template("signup.html", form=form)

@app.route("/test")
def test():
    import requests

    response = requests.get('https://www.boredapi.com/api/activity')

    if response.status_code == 200:
        data = response.json()["activity"]
    else:
        data = "ERROR"

    return render_template("main.html", data=data)

# @app.errorhandler(404)
# @app.errorhandler(500)
# @app.errorhandler(405)
# def handle_error(e):
#     return render_template("custom_error.html", error = e.code)


# @login_manager.user_loader
# def load_user(user):
#     return session.re