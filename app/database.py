from sqlalchemy import Column, String, Integer, Date, Time, create_engine, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
from flask_login import UserMixin

engine = create_engine("sqlite:///app.db?check_same_thread=False", echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class User(Base, UserMixin):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True)
    nickname = Column("nickname", String)
    email = Column("email", String)
    password = Column("password", String)

    def __init__(self, nickname, email, password):
        super().__init__()
        self.nickname = nickname
        self.email = email
        self.password = password



class Event(Base, UserMixin):
    __tablename__ = "events"

    id = Column("id", Integer, primary_key=True)
    date = Column("date", Date)
    time = Column("time", Time, nullable=True)
    header = Column("header", String(80))
    description = Column("description", String(240), nullable=True)
    user = Column("user", Integer, ForeignKey("users.id"))

    def __init__(self, date, time, header, description, user):
        #super().__init__()
        self.date = date
        self.time = time
        self.header = header
        self.description = description
        self.user = user

Base.metadata.create_all(engine)