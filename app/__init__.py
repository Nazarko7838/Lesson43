from flask import Flask

app = Flask(__name__)
app.secret_key = "SoMeThInG"


from app import routes


# flask run --host=0.0.0.0 --port=80