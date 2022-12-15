import requests
import json

# class for GET calls in the API. 
class GetApiCalls:
    def __init__(self) -> None:
        self.api_base_address = "http://localhost:8000/"

    # most basic API call in this api.
    def get_hello_world(self):
        call = self.api_base_address
        response = requests.get(call)
        return response.text

    # Checks to see if a user exists.
    def get_user(self, user):
        call = f"{self.api_base_address}getuser/{user}"
        response = requests.get(call)
        return response.text

    # Gets notes for a user.
    def get_notes(self, user):
        call = f"{self.api_base_address}getnotes/{user}/"
        response = requests.get(call)
        return response.text

    # Gets notes by a status for a user.
    def get_notes_by_status(self, user, status):
        call = f"{self.api_base_address}gettodo/{user}/{status}"
        response = requests.get(call)
        return response.text

class PutApiCalls:
    def __init__(self) -> None:
        self.api_base_address = "http://localhost:8000/"

    def put_create_user(self, user):
        call = f"{self.api_base_address}createuser"
        params = {"name": user}
        params_json = json.dumps(params)
        print(params)
        response = requests.put(call, data=params_json)
        return response.text