import telegram

from ombi import Ombi
from logger import Logger
from environment import Environment


class Query:
    def __init__(self, update: telegram.Update, context: telegram.ext.CallbackContext):
        self.bot = context.bot
        self.chat_id = (update.effective_chat.id,)
        self.text = " ".join(context.args)

    def validate(self):
        return True if self.text else False


class MultiQuery(Query):
    pass


class MovieQuery(Query):
    pass


class TvQuery(Query):
    pass


class MultiSearchResult:
    def __init__(self, obj: dict):
        for key in obj:
            setattr(self, key, obj[key])

    def fetch(self):
        if self.mediaType == "movie":
            return Ombi.fetch_movie()

    @staticmethod
    def results_from_response(response):
        if response is None:
            return None
        results = [MultiSearchResult(item) for item in response]
        Logger.info(f"Deserialized {len(results)} multi results")
        return results


class SearchResult:
    def __init__(self, obj: dict):
        self.title = obj.get("title")
        self.available = obj.get("available")
        self.requested = obj.get("requested")
        self.overview = obj.get("overview")
        self.approved = obj.get("approved")
        self.denied = obj.get("denied")
        self.weight = 0

    def __lt__(self, other):
        return self.weight < other.weight

    def callback_data(self):
        pass

    @staticmethod
    def results_from_response(response):
        pass


class MovieSearchResult(SearchResult):
    def __init__(self, obj: dict):
        Logger.info(f"Contructing MovieSearchResult from object: {obj}")
        super().__init__(obj)
        self.poster_url = None
        if obj.get("posterPath"):
            self.poster_url = Ombi.Images.Poster.format(obj.get("posterPath"))
        self.weight = obj.get("popularity")
        self.tmdb_id = obj.get("theMovieDbId")
        self.date = obj.get("releaseDate")
        self.year = int(self.date.split("-")[0]) if self.date else None

    def requestable(self):
        return not self.available and not self.requested

    def callback_data(self):
        return {"action": "request", "type": "movie", "id": self.tmdb_id}

    @staticmethod
    def results_from_response(response):
        if response is None:
            return None
        results = [MovieSearchResult(item) for item in response]
        Logger.info(f"Deserialized {len(results)} movie results")
        return results


class TvSearchResult(SearchResult):
    def __init__(self, obj: dict):
        super().__init__(obj)
        self.poster_url = None
        if obj.get("posterPath"):
            self.poster_url = obj.get("banner")
        self.weight = float(obj.get("rating"))
        self.tvdb_id = obj.get("theTvDbId")
        self.date = obj.get("firstAired")
        self.year = int(self.date.split("-")[0]) if self.date else None

    def callback_data(self):
        return {"action": "request", "type": "tv", "id": self.tmdb_id}

    @staticmethod
    def results_from_response(response):
        if response is None:
            return None
        return [TvSearchResult(item) for item in response]


class Search:
    @staticmethod
    def execute(query: Query):
        if not query.validate():
            return None

        if isinstance(query, MovieQuery):
            response = Ombi.search_movie(query_str=query.text)
            results = MovieSearchResult.results_from_response(response)
            return results[: Environment.max_search_results()]

        if isinstance(query, MultiQuery):
            response = Ombi.search_multi(query_str=query.text)
            results = MultiSearchResult.results_from_response(response)
            return results[: Environment.max_search_results()]

        return None