from front_functions import GetApiCalls, PutApiCalls

get_api = GetApiCalls()
put_api = PutApiCalls()

print(get_api.get_hello_world())
print(get_api.get_user("Charlie"))
print(get_api.get_user("Renee"))
print(get_api.get_notes("Renee"))
print(get_api.get_notes("charlie"))
print()
print(get_api.get_notes_by_status("Charlie", "In Progress"))
print(get_api.get_notes_by_status("Charlie", "New"))
print(get_api.get_notes_by_status("Renee", "Complete"))
print()
print(put_api.put_create_user("Carrie"))