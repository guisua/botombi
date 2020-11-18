import requests
import json


class Communicator:
    @staticmethod
    def post(url: str, headers: dict, data: dict):
        return requests.post(url=url, json=data, headers=headers).json()

    @staticmethod
    def get(url: str, headers: dict):
        return requests.get(url=url, headers=headers).json()