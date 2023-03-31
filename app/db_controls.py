from sqlalchemy.orm import Session
from .database import User, engine, Event, session
import json
# from database import session, User
from flask import jsonify

session = Session(engine)

def create_json_from(obj):
    event_dict = obj.__dict__

    # Видаляємо ключ "_sa_instance_state", який додає SQLAlchemy
    event_dict.pop('_sa_instance_state', None)

    #Перетворюємо дату та час на рядки, щоб повернути їх користувачу
    event_dict['time'] = event_dict['time'].strftime('%H:%M')
    event_dict['date'] = event_dict['date'].strftime('%Y-%m-%d')

    json_string = json.dumps(event_dict)
    return json_string


def add_new_item(item):
    session.add(item)
    session.commit()

def check_if_user_exists(nickname:str):
    user = session.query(User).where(User.nickname == nickname).first()
    return user


def get_events_by(date):
    events = session.query(Event).filter(Event.date == date, Event.user == 1).all()             #.all()#.where(Event.date == date).all()
    jsonified_events = []
    for event in events:
        jsonified_events.append(create_json_from(event))
    return jsonified_events
