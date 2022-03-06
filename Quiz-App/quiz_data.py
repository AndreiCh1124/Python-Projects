import requests, json

filename = "questions.json"

def json_file_modifier(file, content, action):
    """Function for reading from/writing to json file"""
    if action == "read":
        with open(file, "r") as read_file:
            content = json.load(read_file)
        return content
    if action == "write":
        with open(file, "w") as write_file:
            json.dump(content, write_file, indent=2)

question_data = dict()
question_data = json_file_modifier(filename, question_data, "read")
    