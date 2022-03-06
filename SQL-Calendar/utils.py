import hashlib, re, ezgmail, random, colorama

numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

def string_hasher(element):
    """Return a hash from the passed parameter."""
    element = element.encode()
    element = hashlib.sha512(element).hexdigest()
    return element

def validate_email(email):
    """Checks the email and return a bool acordingly."""
    regex_key = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    if re.fullmatch(regex_key, email):
        return True
    else:
        return False

def validate_phone_nr(phone):
    """Checks the phone number and return a bool acordingly."""
    regex_key = r"07\d\d \d\d \d\d \d\d|07\d\d \d\d\d \d\d\d|07\d\d\d\d\d\d\d\d"
    if re.fullmatch(regex_key, phone):
        return True
    else:
        return False

def generate_code():
    """Generates a 6 digit code for email verifications."""
    code = str()
    for _ in range(6):
        code += random.choice(numbers)
    return str(code)

def send_email_verification(email, action, username=""):
    """Sends an email with the code for various verifications."""
    code = generate_code()
    recipient = email
    subject = "Verification Code"
    message_body = f"""
Hello {username},

Please use this code for your {action} 
confirmation:
    {code}

Your sincerly,
The Events Master Team.
    """
    ezgmail.send(
        recipient=recipient,
        subject=subject,
        body=message_body
    )
    return code

def send_delete_email(email, username):
    """Sends an email to inform the user about account deletion."""
    recipient = email
    subject = "Account Deleted"
    message_body = f"""
Hello {username},

Your account and all your saved events
have been succesfully deleted.

Your sincerly,
The Events Master Team.
    """
    ezgmail.send(
        recipient=recipient,
        subject=subject,
        body=message_body
    )

def send_password_change_email(username, email):
    """Sends an email to inform the user about password cahnge."""
    recipient = email
    subject = "Password Changed"
    message_body = f"""
Hello {username},

Your password has been succesfully changed.

Your sincerly,
The Events Master Team.
    """
    ezgmail.send(
        recipient=recipient,
        subject=subject,
        body=message_body
    )

def colored_print(color, text, action):
    """Prints/Asks for input with colored text."""
    if color == "red":
            style = colorama.Fore.RED
    elif color == "green":
        style = colorama.Fore.GREEN
    elif color == "blue":
            style = colorama.Fore.BLUE
    elif color == "magenta":
        style = colorama.Fore.MAGENTA
    elif color == "lmagenta":
            style = colorama.Fore.LIGHTMAGENTA_EX
    if action == "print":
        print(style + text + colorama.Style.RESET_ALL)
    elif action == "input":
        input_text = input(style + text + colorama.Style.RESET_ALL)
        return input_text

def send_reminder(email):
    pass