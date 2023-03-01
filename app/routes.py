from . import app
from flask import render_template, request, redirect, jsonify, make_response
from flask_login import current_user, login_user, login_required, logout_user, login_manager
from .forms import LoginForm, SignupForm
from .db_controls import get_events_by, add_new_item
from .database import Event, User, session
# from app import login_manager

def commit_new_item(item):
    session.add(item)
    session.commit()
    session.close()

@app.route("/create_event", methods=["POST"])
def create_event():
    data_from_request = request.get_json()
    data_from_request["user"] = current_user.id
    event = Event(**data_from_request)
    add_new_item(event)
    response.status_code = 200
    return response

@app.route("/get_events_by_date/<date>", methods=["GET"])
def get_events_by_date(date):
    data = {"name": "John", "age": 30}
    response = make_response(jsonify(data))
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET')
    response.headers.add('Access-Control-Allow-Headers', '*')
    return response



@app.route("/")
@app.route("/main")
def index():
    return render_template("main.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        name = form.nickname.data
        password = form.password.data

        user_check = session.query(User).where(User.nickname == name).first()

        if not user_check:
            print(name, password)
            return render_template("main.html", message="Login Error!")

        login_user(user_check)
        return render_template("main.html")

    return render_template("login.html", form = form)


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

@app.errorhandler(404)
@app.errorhandler(500)
@app.errorhandler(405)
def handle_error(e):
    return render_template("custom_error.html", error = e.code)
