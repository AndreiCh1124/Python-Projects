import re, logging

logging.basicConfig(
    level=logging.DEBUG,
    format = "%(asctime)s - %(filename)s - %(levelname)s - %(funcName)s - %(message)s",
    filename="log_history.log"
)
def validate_email(email):
    regex_key = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    if re.fullmatch(regex_key, email):
        return True
    else:
        logging.debug(f"Function \"valdiate_email\" was called using \"{email}\" as argument")
        # raise Exception("Invalid argument")
        return False

def validate_name(name):
    temp = str(name).split()
    if len(temp) >= 2:
        for element in temp:
            if len(element) <= 1:
                return False
        return True
    else:
        logging.debug(f"Function was called using \"{name}\" as argument")
        # raise Exception("Invalid argument")
        return False

def validate_phone(phone):
    regex_key = r"07\d\d \d\d \d\d \d\d|07\d\d \d\d\d \d\d\d"
    if re.fullmatch(regex_key, phone):
        return True
    else:
        logging.debug(f"Function \"phone_number_checker\" was called using \"{phone}\" as argument")
        # raise Exception("Invalid argument")
        return False