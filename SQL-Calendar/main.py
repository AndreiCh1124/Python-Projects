import sys, os, signal
from datetime import datetime
from models import create_new_user, delete_account, change_password,\
    login, delete_event, create_new_event, add_event, event_date_input
from utils import colored_print

logged_in = False

clear_console = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')
signal.signal(signal.SIGINT, lambda x, y: sys.exit(0))

def show_menu():
    text1 = """
Here is a list of all the options.
To select an option just type the word specified in the brackets.
    """
    text2 = """
1. See all events(Type "see")
2. Delete event(Type "del_e")   
3. Add event(Type "add")
4. Change password(Type "change")
5. Delete account(Type "del_a")
6. Logout[automatically quits after](Type "logout").
"""
    colored_print("magenta", text1, "print")
    return colored_print("blue", text2, "input")

colored_print("magenta", "Hello and welcome to Events Master.", "print")
colored_print("magenta", "You can quit any time by pressing CTRL + c.", "print")

choice = colored_print("blue", "Do you have an account? Type yes(y)/no(n): ", "input").lower()
if choice == "y" or choice == "yes":
    user_id, username, email, events_list = login()
    logged_in = True
elif choice == "n" or choice == "no":
    colored_print("magenta", "Follow the steps below to create an account.", "print")
    create_new_user()
    colored_print("green", "Account succesfully created.", "print")
    answer = colored_print("blue", "Do you want to login? Type yes(y)/no(n): ", "input").lower()
    if answer == "y" or answer == "yes":
        user_id, username, email, events_list = login()
        logged_in = True
    elif answer == "no" or answer == "n":
        sys.exit()
else:
    colored_print("red", "Unrecognized command.", "print")
clear_console()
while logged_in == True:
    action = show_menu().lower()
    clear_console()
    if action == "see":
        if len(events_list) == 0:
            colored_print("lmagenta", "You do not have any events yet! Use the \"add\" command to add one.", "print")
        else:
            for event in events_list:
                if event.days_left:
                    text = f"{str(event.event_name)}: {event.event_date}, {event.days_left} days remaining."
                else:
                    text = f"{str(event.event_name)}: {event.event_date}, {event.days_left} remaining."
                colored_print("lmagenta", text, "print")
    elif action == "del_e":
        event_name = colored_print("blue", "Please type the name of your event: ", "input")
        delete_event(event_name)
        colored_print("green", "Succsessfully deleted event.", "print")
    elif action == "add":
        event_name = add_event().name
        date_input = event_date_input()
        datetime_object = datetime.strptime(f'{date_input.day} {date_input.hour}:{date_input.minute}{date_input.am_pm} {date_input.month} {date_input.year}', '%d %I:%M%p %b %Y')
        create_new_event(event_name, datetime_object, username=username)
    elif action == "change":
        change_password(username, email)
    elif action == "del_a":
        delete_account(username)
        logged_in = False
    elif action == "logout":
        colored_print("green", text=f"Successfully logged out of {username}", action="print")
        sys.exit()
    else:
        colored_print("red", "Unrecognized command. Please try again.", "print")