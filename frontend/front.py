from front_functions import GetApiCalls

api = GetApiCalls()

print(api.get_hello_world())
print(api.get_user("Charlie"))
print(api.get_user("Renee"))
print(api.get_notes("Renee"))
print(api.get_notes("charlie"))
print()
print(api.get_notes_by_status("Charlie", "In Progress"))
print(api.get_notes_by_status("Charlie", "New"))
print(api.get_notes_by_status("Renee", "Complete"))