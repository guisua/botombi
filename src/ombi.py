from networking import Communicator


class Ombi:

    _ombi = None

    def __init__(self, host: str, api_key: str, ombi_user_name: str):
        self.host = host
        self.api_key = api_key
        self.ombi_user_name = ombi_user_name
        self.headers = {
            "ApiKey": self.api_key,
            "UserName": self.ombi_user_name,
        }

    @staticmethod
    def initialize(host: str, api_key: str, ombi_user_name: str):
        if not host:
            return False
        if not api_key:
            return False
        if not ombi_user_name:
            return False
        Ombi._ombi = Ombi(host=host, api_key=api_key, ombi_user_name=ombi_user_name)
        return True

    def _base_url(self):
        return f"{self.host}/api/v2"

    def _search_url(self):
        return f"{self._base_url()}/search/multi"

    def _search(self, query_str: str):
        url = f"{self._search_url()}/{query_str}"
        data = {"movies": True, "music": False, "people": False, "tvShows": True}
        return Communicator.post(url=url, headers=self.headers, data=data)

    @staticmethod
    def search(query_str: str):
        return Ombi._ombi._search(query_str=query_str)