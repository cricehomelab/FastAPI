import requests
import json
from front_functions import GetApiCalls, PutApiCalls

get = GetApiCalls()
put = PutApiCalls()

def logged_out_options():
    print("1. Create user.")
    print("2. Login user.")
    print("3. Exit.")

def logged_in_options():
    print("1. Add a TODO.")
    print("2. Check TODOs.")
    print("3. logout")

def create_user():
    print("Enter name of the user")
    user = input("username: ")
    response = put.put_create_user(user)
    response = json.loads(response)
    return response["response"]

def login():
    print("Enter your Username.")
    user = input("Username: ")
    response = get.get_user(user)
    response = json.loads(response)
    #print(response)
    if response["message"] == True:
        return (True, user)
    else:
        return (False, user)

main = True
user = ""
logged_in = False
loop = True

while main == True:
    print("Welcome to API Todo.")
    if logged_in == False:        
        while loop:
            print("what would you like to do?")
            logged_out_options()
            choice = input("choice: ")
            if choice == "1":
                print(create_user())
            elif choice == "2":
                response = login()
                logged_in = response[0]
                attempt_user = response[1]
                if logged_in == False:
                    print(f"Login failed for {user}.")
                else:
                    user = attempt_user
                    break
            elif choice == "3":
                loop = False
                main = False
            else:
                print("invalid choice")
    elif logged_in == True:
        print(f"you are logged in {user}")
        while logged_in == True:
            print(f"What would you like to do {user}")
            logged_in_options()
            response = input("Choice: ")
            if response == "3":
                logged_in = False
                break
    else:
        break