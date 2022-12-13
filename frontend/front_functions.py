import requests

class ApiCalls:
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