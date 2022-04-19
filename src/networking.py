import requests
import json

from logger import Logger


class Communicator:
    @staticmethod
    def post(url: str, headers: dict, data: dict):
        Logger.info(f"HTTP POST '{url}' with body: {data}")
        response = requests.post(url=url, json=data, headers=headers).json()
        Logger.info(f"Got response: {response}")
        if hasattr(response, "get") and response.get("errors"):
            return None
        return response

    @staticmethod
    def get(url: str, headers: dict):
        Logger.info(f"HTTP GET '{url}'")
        response = requests.get(url=url, headers=headers).json()
        Logger.info(f"Got response: {response}")
        return response
