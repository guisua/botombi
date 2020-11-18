from networking import Communicator


class Ombi:
    class Images:
        Poster = "https://image.tmdb.org/t/p/w300{}"

    class Endpoint:
        class Search:
            Movie = "/v1/Search/movie/{}"
            Tv = "/v1/Search/tv/{}"
            Multi = "/v2/search/multi/{}"

        class Request:
            Movie = "/v1/Request/movie"

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
        return f"{self.host}/api"

    def _search_multi(self, query_str):
        url = self._base_url() + Ombi.Endpoint.Search.Multi.format(query_str)
        data = {"movies": True, "music": False, "people": False, "tvShows": True}
        return Communicator.post(url=url, headers=self.headers, data=data)

    def _search_movie(self, query_str):
        url = self._base_url() + Ombi.Endpoint.Search.Movie.format(query_str)
        return Communicator.get(url=url, headers=self.headers)

    def _search_tv(self, query_str):
        url = self._base_url() + Ombi.Endpoint.Search.Tv.format(query_str)
        return Communicator.get(url=url, headers=self.headers)

    def _request_movie(self, tmdb_id):
        return Communicator.post(
            url=Ombi.Endpoint.Request.Movie,
            headers=headers,
            data={"theMobieDbId": tmdb_id},
        )

    @staticmethod
    def search(query_str: str):
        return Ombi._ombi._search_movie(query_str=query_str)

    @staticmethod
    def search_movie(query_str: str):
        return Ombi._ombi._search_movie(query_str=query_str)

    @staticmethod
    def search_tv(query_str: str):
        return Ombi._ombi._search_tv(query_str=query_str)

    @staticmethod
    def request_movie(tmdb_id: int):
        return Ombi._ombi._request_movie(tmdb_id=tmdb_id)