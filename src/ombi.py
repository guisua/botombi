from networking import Communicator
from logger import Logger


class Ombi:
    class Images:
        Poster = "https://image.tmdb.org/t/p/w300{}"

    class Endpoint:
        class Search:
            Movie = "/v2/search/Movie/{}"
            Tv = "/v2/search/Tv/{}"
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
        Logger.info(f"Send movie search to Ombi for query '{query_str}'")
        url = self._base_url() + Ombi.Endpoint.Search.Movie.format(query_str)
        return Communicator.get(url=url, headers=self.headers)

    def _search_tv(self, query_str):
        Logger.info(f"Send TV search to Ombi for query '{query_str}'")
        url = self._base_url() + Ombi.Endpoint.Search.Tv.format(query_str)
        return Communicator.get(url=url, headers=self.headers)

    def _request_movie(self, tmdb_id):
        Logger.info(f"Send Movie search to Ombi for tmdb_id '{tmdb_id}'")
        url = self._base_url() + Ombi.Endpoint.Request.Movie
        return Communicator.post(
            url=url,
            headers=self.headers,
            data={"theMovieDbId": tmdb_id},
        )

    @staticmethod
    def search(query_str: str):
        return Ombi._ombi._search_movie(query_str=query_str)

    @staticmethod
    def search_multi(query_str: str):
        return Ombi._ombi._search_multi(query_str=query_str)

    @staticmethod
    def search_movie(query_str: str):
        return Ombi._ombi._search_movie(query_str=query_str)

    @staticmethod
    def search_tv(query_str: str):
        return Ombi._ombi._search_tv(query_str=query_str)

    @staticmethod
    def fetch_movie(tmdb_id: int):
        return Ombi._ombi._search_movie(query_str=str(tmdb_id))

    @staticmethod
    def request_movie(tmdb_id: int):
        Logger.info(f"Requesting movie with id {tmdb_id}")
        return Ombi._ombi._request_movie(tmdb_id=tmdb_id)

    @staticmethod
    def process_callback_data(callback_data):
        if callback_data.action == "request":
            if callback_data.type == "movie":
                Ombi.request_movie(tmdb_id=callback_data.id)
                return
            Logger.info(f"Unsupported callback type '{callback_data.type}'")
            return
        Logger.info(f"Unsupported callback action '{callback_data.action}'")
