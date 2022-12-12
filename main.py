from fastapi import FastAPI
from typing import Union
from data import Database
from pydantic import BaseModel
import datetime as dt

# API object.
app = FastAPI()

# Database creation
db = Database()
conn = db.create_connection(db.database_file)
for table in db.tables:
    db.create_table(conn, table)


class MakeUser(BaseModel):
    name: str

class Note(BaseModel):
    user: str
    note: str

class SetNoteStatus(BaseModel):
    user: str
    noteid: int
    update: str

#GET functions
# Easiest call to make to Ensure the API can be hit.
@app.get("/")
def read_root():
    return {"Message": "API for TODO list."}

# Checks if a user exists.
@app.get("/getuser/{user_id}/")
async def get_user(user_id: str):
    user_id = user_id.lower()
    check_for_user = db.user_exists(conn, user_id)
    # The user_exists() function will return None if a user is not found. 
    if check_for_user == None:
        return {"message": f"User {user_id} not found. Instead got {check_for_user}. "}
    else:
        return {"message": f"{check_for_user} exists."}

# returns notes for a user if they are present. This pulls ALL notes. 
@app.get("/getnotes/{user_id}/")
async def get_notes(user_id: str):
    user_id = user_id.lower()
    check_for_user = db.user_exists(conn, user_id)
    # The user_exists() function will return None if a user is not found.
    if check_for_user == None:
        return {"message": f"User {user_id} not found. Instead got {check_for_user}. "}
    else:
        notes = db.get_notes(conn, check_for_user)
        return {"notes": notes}

# gets todo items based on the user and then the status.
@app.get("/gettodo/{user_id}/{status}")
async def get_notes_by_status(user_id: str, status: str):
    user_id = user_id.lower()
    check_for_user = db.user_exists(conn, user_id)
    # The user_exists() function will return None if a user is not found.
    if check_for_user == None:
        return {"message": f"User {user_id} not found. Instead got {check_for_user}. "}
    else:
        notes = db.get_notes_by_status(conn, check_for_user, status)
        return {"notes": notes}

# PUT functions

# Creates a user.
@app.put("/createuser/")
async def create_user(user: MakeUser): 
    user.name = user.name.lower()   
    check_for_user = db.user_exists(conn, user.name)
    # The user_exists() function will return None if a user is not found.
    if check_for_user == None:
        db.add_user(conn, user.name.lower(), dt.datetime.now())
        check_for_user = db.user_exists(conn, user.name)
        return {"response" : db.user_exists(conn, user.name)}
    else:
        return{"response": f"{check_for_user} exists already. User not added."}

# adds a TODO item to a user's list.
@app.put("/addtodo/")
async def add_note(note: Note):
    note.user = note.user.lower()
    time = dt.datetime.now()
    db.add_note(conn, note.user, note.note, time)
    return {"message": "true"}

# Set the status of a note from what it is to something else.
@app.put("/setstatus/")
async def set_note_status(status: SetNoteStatus):
    update = db.update_status(conn, status.user, status.noteid, status.update)
    return {"message": update}