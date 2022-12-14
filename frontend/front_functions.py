import requests

class GetApiCalls:
    def __init__(self) -> None:
        self.api_base_address = "http://localhost:8000/"

    def get_hello_world(self):
        call = self.api_base_address
        response = requests.get(call)
        return response.text

    def get_user(self, user):
        call = f"{self.api_base_address}getuser/{user}"
        response = requests.get(call)
        return response.text
    
    def get_notes(self, user):
        call = f"{self.api_base_address}getnotes/{user}/"
        response = requests.get(call)
        return response.text
    
    def get_notes_by_status(self, user, status):
        call = f"{self.api_base_address}gettodo/{user}/{status}"
        response = requests.get(call)
        return response.text

class PutApiCalls:
    def __init__(self) -> None:
        pass