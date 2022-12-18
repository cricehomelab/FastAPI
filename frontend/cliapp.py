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

def todo_options():
    print("1. See Notes in 'New' status.")
    print("2. See notes in 'In Progress' status.")
    print("3. See notes in 'Complete' status.")

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

def note_formatter(notes):
    notes = notes['notes']
    new_notes = {}
    for num, note in enumerate(notes):
        new_notes[num] = {}
        new_notes[num]["id"] = note[0]
        new_notes[num]["user_id"] = note[1]
        new_notes[num]['todo_note'] = note[2]
        new_notes[num]['todo_staus'] = note[3]
        new_notes[num]['todo_duedate'] = note[4]
        new_notes[num]['date_added'] = note[5]
        new_notes[num]['date_modified'] = note[6]
        new_notes[num]['date_completed'] = note[7]
    for note in new_notes:
        print()
        todo_item = new_notes[note]
        for item in todo_item:
            print(f"{item}: {todo_item[item]}")
        

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
            response = ""
            print(f"What would you like to do {user}")
            logged_in_options()
            response = input("Choice: ")
            if response == "1":
                print("What ToDo would you like to add?")
                todo = input("TODO: ")
                response = put.put_add_todo(user, todo)
                response = json.loads(response)
                print(f"TODO added for {response['user']}\nTODO is: {response['todo']}\nTODO is due on: {response['duedate']}")
            if response == "2":
                response = ""
                todo_options()
                response = input("Choice: ")
                if response == "1":
                    notes = get.get_notes_by_status(user,"New")
                    #print(notes)
                    notes = json.loads(notes)
                    note_formatter(notes)
            elif response == "3":
                logged_in = False
                user = ""
                break
    else:
        break