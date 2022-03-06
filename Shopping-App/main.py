import sys, datetime, random, json, hashlib
from user_interactions.utils import validate_email, validate_name, validate_phone

greetings = ("Hello!", "Hi there!", "Hey, welcome!")
name_asking = ("What's your name? ", "Please type your name: ", "Can you tell me your name? ")
age_asking = ("What's your age? ", "Please type your age: ", "Can you tell me your age? ")
list_avalaibilty_asking = ("Do you have a list?(y/n) ", "Have you brought a list?(y/n) ", \
                            "Is there any list?(y/n) ")
positive_answers = ("Great! ", "I'll bring them now. ", "There you go. ", "Here are your products!")
neagtive_answers = ("Please come back with a list. ", "No list? Really? ", "No list, no party! ")
forbidden_items = ("beer", "cigars", "wine")
prods_file = 'products.json'
logins_file = "logins.json"
logins_dict = dict()
available_items = list()
total_price = 0
list_of_items = list()
prods_available = list()

def string_hasher(item):
    item = str(item).encode()
    return hashlib.sha3_512(item).hexdigest()

def time_calculator(seconds):
    time = datetime.timedelta(seconds = seconds)
    updated_time = (datetime.datetime.now() + datetime.timedelta(seconds = seconds)).strftime('%H:%M:%S')
    return time, updated_time

def json_file_handler(content, file, action):
    if action == "read":
        with open(file, "r") as read_file:
            content = json.load(read_file)
        return content
    if action == "write":
        with open(file, "w") as write_file:
            json.dump(content, write_file, indent=2)

def new_client_handler(logins_dict):
    logins_dict = json_file_handler(logins_dict, logins_file, "read")
    name = input(random.choice(name_asking))
    while validate_name(name) != True:
        name = input("Invalid name. Try again: ")
    age = int(input(random.choice(age_asking)))
    while not (age > 10 and age < 100):
        print(f"False age: {age}. Please type your age again.")
        age = int(input())
    email = input("Please your email adress: ")
    while validate_email(email) != True:
        email = input("Invalid email. Type a valid one. ")
    phone_number = input("Please type your phone number: ")
    while validate_phone(phone_number) != True:
        phone_number = input("Invalid phone number. Type a valid one: ")
    username = input("Please type a username ")
    while username in logins_dict:
        username = input(f"{username} is already taken. Try another one: ")
    password = string_hasher(input("Please type a password "))
    logins_dict[username] = {
    "name": name,
    "age": age,
    "email": email,
    "phone": phone_number,
    "password": password
}
    json_file_handler(logins_dict, logins_file, "write")
    return age

def password_change_funtion(logins_dict, username):
    flag_check = True
    logins_dict = json_file_handler(logins_dict, logins_file, "read")
    print("To verify your identy please type your age and email: ")
    user_age = int(input("Age: "))
    user_email = input("Email: ")
    if user_age != logins_dict[username]["age"]:
        flag_check = False
    if user_email != logins_dict[username]["email"]:
        flag_check = False
    if flag_check == True:
        new_password = string_hasher(input("Enter your new password: "))
        logins_dict[username]["password"] = new_password
        json_file_handler(logins_dict, logins_file, "write")
    else:
        print("Failed verification. \nAcces denied.")
        sys.exit()

def old_client_handler(logins_dict):
    tries = 0
    logins_dict = json_file_handler(logins_dict, logins_file, "read")
    username = input("Please enter your username: ")
    while username not in logins_dict:
        username = input(f"Username {username} not found. Try again. ")
    password = string_hasher(input("Please enter your password: "))
    while password != logins_dict[username]["password"]:
        logins_dict = json_file_handler(logins_dict, logins_file, "read")
        password = string_hasher(input("Incorrect password. Try again: "))
        tries += 1
        if tries == 4:
            answer = input("Do you want to change your password?(y/n) ")
            if answer == "y":
                password_change_funtion(logins_dict, username)
                logins_dict = json_file_handler(logins_dict, logins_file, "read")
                password = string_hasher(input("Please type your new password: "))
            else:
                print("Suspicious activity detected :()")
                sys.exit()
    print(f"Welcome back, {str(logins_dict[username]['name']).title()}")
    return logins_dict[username]["age"]

def menu_printer(prod_dict):
    print("Here's a list of all available items: ")
    for key in prod_dict:
        print(f"{str(key).ljust(20, '.')}{str(prod_dict[key]['price']).rjust(4)}$")

def robot_verification(name):
    secret_key = name
    temp_nr_list = list()
    verification = True
    for idx in range(len(secret_key)):
        temp_nr_list.append(idx)
    name_sample_1, name_sample_2 = random.choices(temp_nr_list, k=2)
    while name_sample_1 == name_sample_2:
        name_sample_1 = random.choice(temp_nr_list)
    name_check_1 = input(f"Please type the letter at position {name_sample_1+1} from your name:  ")
    name_check_2 = input(f"Please type the letter at position {name_sample_2+1} from your name:  ")
    if name_check_1 != secret_key[name_sample_1]:
        verification = False
    if name_check_2 != secret_key[name_sample_2]:
        verification = False
    if verification == False:
        print("Failed verification! \n Acces denied!")
        sys.exit()
    else:
        print("Acces granted!")

answer = input("Do you have an account?(y/n) ")
if answer == "y":
    age = old_client_handler(logins_dict)
elif answer == "n":
    age = new_client_handler(logins_dict)
else:
    print("Error. Unknown character. ")
    sys.exit()

have_list = input(random.choice(list_avalaibilty_asking))
if have_list != "y":
    print(random.choice(neagtive_answers))
    sys.exit()
available_items = json_file_handler(available_items, prods_file, "read")
menu_printer(available_items)

while True:
    products = input("Please type a product: ").lower().split(" ")
    if products[0] in ["", "nimic", "nothing", " "]:
        break
    else:
        for product in products:
            if age < 18 and product in forbidden_items:
                print(f"You are not allowed to purchase {product} :)))")
            elif product in available_items:
                list_of_items.append(product)
                total_price += available_items[product]['price']
            elif product not in ["", "nimic", "nothing", " "]:
                print(f"{product.capitalize()} is not on the menu")

if len(list_of_items) >= 2:
    random_item_not_available = random.choice(list_of_items)
    print(f"Unfortunately, we don't have any {random_item_not_available} on stock...")
    list_of_items.remove(random_item_not_available)
    total_price -= int(available_items[random_item_not_available]['price'])

if len(list_of_items) != 0:
    time_to_wait, time_to_arrive = time_calculator((len(list_of_items))*30)
    print(random.choice(positive_answers))
    print(f"You gotta pay a total of {total_price}$")
    print(f"You will have to wait {time_to_wait}.")
    print(f"You can return after {time_to_arrive} to get your products.")