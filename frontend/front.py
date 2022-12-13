from front_functions import ApiCalls

api = ApiCalls()

print(api.get_hello_world())
print(api.get_user("Charlie"))
print(api.get_user("Renee"))

