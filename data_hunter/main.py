import os
import csv
import typing as t
from pathlib import Path
from fzmovies_api import Search
from fzmovies_api.filters import MovieGenreFilter


class MovieDataHunter:

    field_names = (
        "genre",
        "category",
        "title",
        "year",
        "distribution",
        "description",
        "url",
        "cover_photo",
    )

    def __init__(
        self,
        genres: t.List[
            t.Literal[
                "Action",
                "Adventure",
                "Animation",
                "Biography",
                "Comedy",
                "Crime",
                "Documentary",
                "Drama",
                "Family",
                "Fantasy",
                "Film-Noir",
                "History",
                "Horror",
                "Music",
                "Musical",
                "Mystery",
                "Romance",
                "Sci-Fi",
                "Sport",
                "Thriller",
                "War",
                "Western",
            ]
        ] = ["_"],
        categories: t.List[t.Literal["Bollywood", "Hollywood"]] = ["_"],
    ):
        """

        Args:
            name (t.Literal['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime',
            'Documentary', 'Drama', 'Family', 'Fantasy', 'Film-Noir', 'History', 'Horror', 'Music',
            'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Sport', 'Thriller', 'War', 'Western'], optional):
            Movie genre name. Defaults to "_" (all).
            category (t.Literal["Bollywood", "Hollywood"], optional): Movie category. Defaults to "_" (all).
        """
        self.genres = MovieGenreFilter.available_genres if genres == ["_"] else genres
        self.categories = (
            ["Hollywood", "Bollywood"] if categories == ["_"] else categories
        )

    def hunt(
        self,
        dir: t.Union[Path, str] = os.getcwd(),
        prefix: str = "",
        limit: int = 1_000_000,
        stream: bool = False,
    ) -> t.Union[t.Dict, t.Generator[t.Tuple, None, None]]:
        """Hunt down matches and save them to the specified path.

        Args:
            dir (t.Union[Path, str], optional): Parent directory to save the datasets to. Defaults to os.getcwd().
            prefix (str, optional): Datasets filename prefix. Defaults to ''.
            limit (int, optional): Total movies (multiple of 20). Defaults to 1_000_000.
            stream (bool, optional): Yield the paths. Defaults to False. Defaults to False.

        Returns:
            t.Union[t.Dict, t.Generator[t.Tuple, None, None]] : Path to datasets harvested.
        """

        def hunt_movies():
            for category in self.categories:
                for genre in self.genres:
                    movies_count = 0
                    search = Search(
                        query=MovieGenreFilter(name=genre, category=category)
                    )
                    saved_to = Path(
                        os.path.join(dir, prefix + genre.casefold() + ".csv")
                    )
                    write_mode = "a" if saved_to.exists() else "w"
                    with open(saved_to, write_mode) as fh:
                        writer = csv.DictWriter(fh, fieldnames=self.field_names)
                        if write_mode == "w":
                            writer.writeheader()
                        for result in search.get_all_results(stream=True, limit=limit):
                            movies_count += len(result.movies)
                            movie_items: t.List[t.Dict[str, str]] = []
                            for movie in result.movies:
                                movie_items.append(
                                    dict(
                                        genre=genre,
                                        category=category,
                                        title=movie.title,
                                        year=movie.year,
                                        distribution=movie.distribution,
                                        description=movie.about,
                                        url=movie.url,
                                        cover_photo=movie.cover_photo,
                                    )
                                )
                            writer.writerows(movie_items)
                            yield category, genre, movies_count, len(
                                result.movies
                            ), saved_to

        def default():
            cache = {
                "total_movies": 0,
                "category": [],
                "genres": [],
                "saved_to": [],
                "genre_count": {},
            }
            for category, genre, movies_count, newly_saved, saved_to in hunt_movies():
                cache["total_movies"] += newly_saved
                cache["genre_count"][genre] = movies_count
                cache["movies_count"] += movies_count
                cache["genres"].append(genre)
                cache["saved_to"].append(saved_to)
                if not category in cache["category"]:
                    cache["category"].append(category)

            return cache

        return hunt_movies() if stream else default()
