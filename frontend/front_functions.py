import requests

class ApiCalls:
    def __init__(self) -> None:        
        self.api_base_address = "http://localhost:8000/"


    def hello_world(self):
        response = requests.get(self.api_base_address)
        print(response.text)
        