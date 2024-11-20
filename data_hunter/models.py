"""SQLModels for relational and non-relational tables
"""

from sqlmodel import SQLModel, Field, Relationship, Column, Text


class UnformmatedMovies(SQLModel, table=True):
    """This is a complete model with no relation
    with other models
    """

    __tablename__ = "movies"
    index: int | None = Field(None, primary_key=True)
    genre: str
    category: str
    title: str
    year: int
    distribution: str
    description: str
    url: str
    cover_photo: str

    def __repr__(self):
        return f"{self.title} ({self.year})"


class MovieGenre(SQLModel, table=True):
    """Joins Genre and Movies"""

    __tablename__ = "movie_genre"
    id: int | None = Field(None, primary_key=True)
    movie_id: int | None = Field(None, foreign_key="movie.id")
    genre_id: int | None = Field(None, foreign_key="genre.id")

    def __repr__(self):
        return f"<MovieId={self.movie_id}, GenreId={self.genre_id}"


class Genre(SQLModel, table=True):
    """Movie genre"""

    __tablename__ = "genre"
    id: int | None = Field(None, primary_key=True)
    name: str | None = Field(None, unique=True)
    movies: list["Movie"] = Relationship(back_populates="genres", link_model=MovieGenre)

    def __repr__(self):
        return self.name


class Category(SQLModel, table=True):
    """Movie category"""

    __tablename__ = "category"
    id: int | None = Field(None, primary_key=True)
    name: str | None = Field(None, unique=True)
    movies: list["Movie"] = Relationship(
        back_populates="category", cascade_delete=True, passive_deletes=True
    )

    def __repr__(self):
        return self.name


class Movie(SQLModel, table=True):
    """Movie model"""

    __tablename__ = "movie"
    id: int | None = Field(
        None,
        primary_key=True,
    )
    title: str | None = Field(None, unique=True)
    year: int
    distribution: str | None
    description: str | None = Field(None, sa_column=Column(Text, default=None))
    url: str | None = Field(None, unique=True)
    cover_photo: str | None = Field(None)
    category: Category | None = Relationship(back_populates="movies")
    genres: list["Genre"] = Relationship(back_populates="movies", link_model=MovieGenre)
    category_id: int | None = Field(None, foreign_key="category.id")

    def __repr__(self):
        return f"{self.title} ({self.year})"
