from networking import Communicator
from logger import Logger


class Ombi:
    class Images:
        Poster = "https://image.tmdb.org/t/p/w300{}"

    class Endpoint:
        class Search:
            Movie = "/v2/search/Movie/{}"
            Tv = "/v2/search/Tv/moviedb/{}"
            Multi = "/v2/search/multi/{}"

        class Request:
            Movie = "/v1/Request/movie"
            Tv = "/v2/Requests/tv"

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
        Logger.info(f"Send Movie request to Ombi for tmdb_id '{tmdb_id}'")
        url = self._base_url() + Ombi.Endpoint.Request.Movie
        return Communicator.post(
            url=url,
            headers=self.headers,
            data={"theMovieDbId": tmdb_id},
        )

    def _request_tv(self, themoviedb_id):
        Logger.info(f"Send TV Show request to Ombi for themoviedb_id '{themoviedb_id}'")
        url = self._base_url() + Ombi.Endpoint.Request.Tv
        return Communicator.post(
            url=url,
            headers=self.headers,
            data={"requestAll": True, "theMovieDbId": themoviedb_id},
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
    def fetch_tv(thetvdb_id: int):
        return Ombi._ombi._search_tv(query_str=str(thetvdb_id))

    @staticmethod
    def request_movie(tmdb_id: int):
        if tmdb_id is None:
            Logger.error(f"Tried to request movie with id: {tmdb_id}")
            return False
        Logger.info(f"Requesting movie with id: {tmdb_id}")
        response = Ombi._ombi._request_movie(tmdb_id=tmdb_id)
        if response is not None:
            if response.get("isError") == False:
                return response.get("result")
            Logger.error(response.get("errorMessage"))
        return None

    @staticmethod
    def request_tv(themoviedb_id: int):
        if themoviedb_id is None:
            Logger.error(f"Tried to request TV show with id: {themoviedb_id}")
            return False
        Logger.info(f"Requesting TV show with id: {themoviedb_id}")
        response = Ombi._ombi._request_tv(themoviedb_id=themoviedb_id)
        if response is not None:
            if response.get("isError") == False:
                return response.get("result")
            Logger.error(response.get("errorMessage"))
        return None

    @staticmethod
    def process_callback_data(callback_data):
        if callback_data.action == "request":
            if callback_data.type == "movie":
                return Ombi.request_movie(tmdb_id=callback_data.id)
            if callback_data.type == "tv":
                return Ombi.request_tv(themoviedb_id=callback_data.id)
            Logger.info(f"Unsupported callback type '{callback_data.type}'")
            return None
        Logger.info(f"Unsupported callback action '{callback_data.action}'")
        return None
