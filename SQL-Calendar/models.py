from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Date
from datetime import datetime, date

from utils import string_hasher, validate_phone_nr, validate_email, \
    send_email_verification, send_delete_email, send_password_change_email, \
    colored_print

DATABASE_URI = ''
engine = create_engine(DATABASE_URI)

Base = declarative_base()

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    email = Column(String)
    phone_number = Column(String)
    events = relationship('Events', backref='users', lazy=False)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def add_username():
    """This function gets a username from the user and checks if it's not taken."""
    input_username = colored_print("blue", "Please type your desired username: ", "input")
    while session.query(Users).filter(Users.username==input_username).first() != None:
        input_username = colored_print("red", "This username is already taken. Try another one: ", "input")
    return input_username

def add_password():
    input_password = colored_print("blue", "Please create a strong password: ", "input")
    return string_hasher(input_password)

def add_phone():
    input_phone = colored_print("blue", "Please type your phone number: ", "input")
    while validate_phone_nr(input_phone) == False:
        input_phone = colored_print("red", "Invalid phone number. Please try again: ", "input")
    return input_phone

def add_email():
    input_email = colored_print("blue", "Please type your email: ", "input")
    while validate_email(input_email) == False:
        input_email = colored_print("red", "Invalid email. Please try again: ", "input")
    codes_flag = check_codes(input_email, "account creation ")
    while codes_flag == False:
        colored_print("red", "Codes don't mactch. Please try again.", "print")
        codes_flag = check_codes(input_email, "account creation ")
    return input_email

def create_new_user():
    new_user = Users(
        username = add_username(),
        password = add_password(),
        email = add_email(),
        phone_number = add_phone(),
    )
    session.add(new_user)
    session.commit()

def validate_identity():
    username = colored_print("blue", "Please type your username: ", "input")
    while session.query(Users).filter(Users.username==username).first() == None:
        username = colored_print("red", "Username not found. Please try again: ", "input")
    password = colored_print("blue", "Please type your password: ", "input")
    while session.query(Users).filter(Users.password==string_hasher(password)).first() == None:
        password = colored_print("red", "Wrong password. Please try again: ", "input")
    email = session.query(Users).filter(Users.username==username).first().email
    return username, email

def login():
    username, email = validate_identity()
    colored_print("green", f"Succesfully logged in as {username}", "print")
    user_id = session.query(Users).filter(Users.username==username).first().id
    events_list = session.query(Users).filter(Users.username==username).first().events
    return user_id, username, email, events_list

def check_codes(email, action, username=""):
    sent_code = str(send_email_verification(email, action=action, username=username))
    input_code = str(colored_print("blue", "Please enter the code you received on your email adress: ", "input"))
    if input_code == sent_code:
        status_flag = True
    else:
        status_flag = False
    return status_flag

def delete_account(username):
    colored_print("magenta", "Are you sure you want to delete your account? This action is ireversible!!", "print")
    confirm = colored_print("blue", "Do you want to proceed(y/n): ", "input").lower()
    if confirm == "y":
        account = session.query(Users).filter(Users.username==username).first()
        user_id = session.query(Users).filter(Users.username==username).first().id
        events = session.query(Events).filter(Events.user_id==user_id)
        email = account.email
        username = account.username
        if check_codes(email, "account deletion ", username) == True:
            session.delete(account)
            for event in events:
                session.delete(event)
            session.commit()
            send_delete_email(email, username)
            colored_print("green", "Account succesfully deleted.", "print")

def handle_password_change(username):
    password = colored_print("blue", "Please enter the new password: ", "input")
    password2 = colored_print("blue", "Please re-enter the new password: ", "input")
    while password != password2:
        colored_print("red", "Passwords don't match. Try again.", "print")
        password = colored_print("blue", "Please enter the new password: ", "input")
        password2 = colored_print("blue", "Please enter the new password: ", "input")
    account = session.query(Users).filter(Users.username==username).first()
    account.password = string_hasher(password)
    session.commit()

def change_password(username, email):
    if check_codes(email, "password change ", username=username) == True:
        handle_password_change(username)
        colored_print("Green", "Succesufully changed password.", "print")
        send_password_change_email(username, email)
    else:
        colored_print("red", "Wrong code. Please try again later.", "print")

# Events =========================================
class Events(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    event_name = Column(String)
    event_date = Column(Date)
    days_left = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))


class EventDate:
    def __init__(self):
        self.day = colored_print("blue", "Day: ", "input")
        self.month = colored_print("blue", "Month(For example type \"jan\" for january): ", "input").title()
        self.year = colored_print("blue", "Year: ", "input")
        self.hour = colored_print("blue", "Please eneter a hour between 1 and 12: ", "input")
        self.am_pm = str(colored_print("blue", "Am or Pm: ", "input")).lower()
        self.minute = colored_print("blue", "Minute: ", "input")

def event_date_input():
    return EventDate()

class EventData:
    def __init__(self):
        self.name = colored_print("blue", "Please enter your new event's title: ", "input")

def add_event():
    return EventData()

def days_left(datetime_object):
    left = abs(datetime_object - datetime.now())
    if left.days >= 1:
        print('Days left: ', left.days)
        return left.days
    else:
        return left

def delete_event(event_name):
    event = session.query(Events).filter(Events.event_name==event_name).first()
    session.delete(event)
    session.commit()

def create_new_event(event_name, datetime_object, username):
    user_id = session.query(Users).filter(Users.username==username).first().id
    new_event = Events(
        event_name = event_name,
        event_date = datetime_object,
        days_left = days_left(datetime_object),
        user_id = user_id
    )
    session.add(new_event)
    session.commit()

# event_frequency()
# create_new_event(event_name, datetime_object, username="andrei_ch")