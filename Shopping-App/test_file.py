def verify_name(name):
    temp = str(name).split()
    if len(temp) >= 2:
        for element in temp:
            if len(element) <= 1:
                return False
        return True
    else:
        raise Exception("This is an invalid name!!")

print(verify_name("Andrei Chr"))
print(verify_name("Jack Lee"))
print(verify_name("123 123"))
