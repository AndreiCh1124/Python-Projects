import random, json, sys, os, hashlib

alph = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', \
        'j', 'k', 'l','z', 'x', 'c', 'v', 'b', '1', '2', '3', '4', '5', '6', '7','8', '9', \
        'n', 'm', 'B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M','N', 'P', 'Q', 'R', 'S', 'T', 'V', 'X',\
        'A', 'E', 'I', 'O', 'U', '@', '!', '%', '^', '&', '*', '(', ')', '-','$', 'Z', 'W', 'Y']

temp_nr_list = list()
key = str()
pass_word_dict = dict()
encrypt_level = 6      #number of numbers used for encryption
password_length = 6
file_with_passwords = "password_data.json"

def json_file_modifier(file, content, action):
    """Function for reading from/writing to json file"""
    if action == "read":
        with open(file, "r") as read_file:
            content = json.load(read_file)
        return content
    if action == "write":
        with open(file, "w") as write_file:
            json.dump(content, write_file, indent=2)

def string_hasher(item):
    """Returns a hash from a string so it can be stored safer"""
    item = str(item).encode()
    item = hashlib.sha3_512(item).hexdigest()
    return item

def generate_key():
    """Generates a radndom string if the user doesn't provide a password"""
    word = ''
    for i in range(0,password_length):
        char = random.choice(alph)
        word += char
    return(word)

def get_encrypt_method(dict_list):
    """ 
        Generates a random password, a set of numbers used for encryption and stores them. \n
        Used if the user doesn't provide a password.
    """
    dict_list = list()
    password = generate_key()
    print(f"Your password is: {password}")
    for _ in range(0, encrypt_level):                     
        nr = random.randint(1,255)
        dict_list.append(nr)
    password = string_hasher(password)
    pass_word_dict[password] = dict_list
    json_file_modifier(file_with_passwords, pass_word_dict, "write")
    return pass_word_dict[password]

def get_password_from_user(dict_list, password):
    """ 
        Generates a random set of numbers used for encryption and stores them. \n
        Used if the user provides a password.
    """
    dict_list = list()
    for _ in range(0, encrypt_level):                     
        nr = random.randint(1,255)
        dict_list.append(nr)
    password = string_hasher(password)
    pass_word_dict[password] = dict_list
    json_file_modifier(file_with_passwords, pass_word_dict, "write")
    return pass_word_dict[password]

def file_type_checker(filename, found_files):
    """Searches recursively for all the subfolders and folders if the filename provided is a directory"""
    path_of_file = os.path.abspath(filename)
    if os.path.isdir(path_of_file) == True:
        for entry in os.scandir(filename):
            if os.path.isdir(os.path.abspath(entry)) == True:
                file_type_checker(entry, found_files)
            if os.path.isdir(entry) == False or os.path.isfile(entry) == True:
                found_files.append(os.path.abspath(entry))
    elif os.path.isfile(path_of_file) == True:
        found_files.append(os.path.abspath(filename))
    return found_files

def file_modification_handler(filename, key):
    """
        This is the general function for encrypt/decrypt.
        It uses an XOR gate to modify the bytes of the file, encrypting/decrypting it.
    """
    file = open(filename, "rb")
    data = file.read()
    file.close()
    data = bytearray(data)
    for index, value in enumerate(data):
        data[index] = value ^ key
    file = open(filename, "bw")
    file.write(data)
    file.close()

def encrypt(filename, key, encrypt_list):
    """Encrypts the file"""
    for k in range(0, encrypt_level):
        key = encrypt_list[k]
        file_modification_handler(filename, key)

def decrypt(filename, key):
    "Decrypts the file"
    final_list = pass_word_dict[hashed_password_received]
    final_list.reverse()
    for a in range(0, encrypt_level):
        key = final_list[a]
        file_modification_handler(filename, key)

while True:
    """
        This is the driver code.
        It gets input from the user and handles the responses
    """
    json_file_modifier(file_with_passwords, pass_word_dict, "read")
    action = input("Do you want to encrypt(e) or decrypt(d) or quit(q)? ")
    if action == "e":
        found_files_list = list()
        temp_encrypt_list = list()
        key = ''
        filename = input("Please enter a filename: ")
        password_from_user = input("Please enter a password for your file/files(leave blank if you want it autogenerated): ")
        if password_from_user == " " or password_from_user == "":
            temp_encrypt_list = get_encrypt_method(temp_encrypt_list)
        else:
            temp_encrypt_list = get_password_from_user(temp_encrypt_list, password_from_user)
        found_files_list = file_type_checker(filename, found_files_list)
        if len(found_files_list) == 1:
            encrypt(filename, key, temp_encrypt_list)
        else:
            for file in found_files_list:
                encrypt(file, key, temp_encrypt_list)
    elif action == "d":
        found_files_list = list()
        filename = input("Please enter a filename: ")
        password_received = input("Please enter your password: ")
        hashed_password_received = string_hasher(password_received)
        found_files_list = file_type_checker(filename, found_files_list)
        if hashed_password_received in pass_word_dict:
            if len(found_files_list) == 1:
                temp_nr_list = list(pass_word_dict[hashed_password_received])
                decrypt(filename, key)
                pass_word_dict.pop(hashed_password_received)
                json_file_modifier(file_with_passwords, pass_word_dict, "write")
            else:
                for file in found_files_list:
                    decrypt(file, key)
                pass_word_dict.pop(hashed_password_received)
                json_file_modifier(file_with_passwords, pass_word_dict, "write")
        else:
            print("Password was not found...")
    elif action ==  "q":
        sys.exit()
    else:
        print("Unrecognized command. Please try again." + "\n")