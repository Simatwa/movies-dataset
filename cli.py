#!/usr/bin/python3

import click
import os
import sys
import pandas
import glob
import sqlite3
import logging
from sqlmodel import (
    SQLModel,
    create_engine,
    Field,
    Relationship,
    select,
    Session,
    Text,
    Column,
)

logging.basicConfig(
    format="%(asctime)s - %(levelname)s : %(message)s",
    datefmt="%d-%b-%Y %H:%M:%S",
    level=logging.INFO,
)

get_exception_string = lambda e: e.args[1] if e.args and len(e.args) > 1 else str(e)
"""Get the excption message"""


@click.group()
def data_hunter():
    """Manipulate .csv data generated accordingly"""


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


class DatabaseRelater:

    @staticmethod
    @click.command()
    @click.argument(
        "db_path", type=click.Path(exists=True, dir_okay=False), metavar="INPUT"
    )
    @click.argument(
        "save_to",
        type=click.Path(dir_okay=False),
        metavar="OUTPUT",
    )
    def relate_tables(db_path, save_to):
        """Recreate a relational-based database, relating movie, genre and category tables"""
        new_engine = create_engine(f"sqlite:///{save_to}")
        logging.info("Creating tables")
        SQLModel.metadata.create_all(new_engine)
        from fzmovies_api.filters import MovieGenreFilter

        with Session(new_engine) as session:
            # Let's insert all the genres & categories available to db
            for genre in MovieGenreFilter.available_genres:
                session.add(Genre(name=genre))
            for category in ["Bollywood", "Hollywood"]:
                session.add(Category(name=category))
            session.commit()
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            logging.info("Loading movie titles")
            cursor.execute("SELECT DISTINCT title FROM Movies;")
            all_titles: list[str] = set([entry[0] for entry in cursor.fetchall()])
            logging.info("Setting-up category mapper")
            category_map = {
                "Hollywood": session.exec(
                    select(Category).where(Category.name == "Hollywood")
                ).first(),
                "Bollywood": session.exec(
                    select(Category).where(Category.name == "Bollywood")
                ).first(),
            }
            logging.info(f"Total titles loaded ({len(all_titles)})")
            with click.progressbar(
                all_titles,
                label="Processing",
                item_show_func=lambda v: v,
                file=sys.stderr,
            ) as progress:
                for title in progress:
                    cursor.execute(
                        f'SELECT DISTINCT genre FROM Movies WHERE title="{title}"'
                    )
                    genres: list[Genre] = [
                        session.exec(
                            select(Genre).where(Genre.name == entry[0])
                        ).first()
                        for entry in cursor.fetchall()
                    ]
                    cursor.execute(
                        "SELECT year, category,  distribution, description, url, "
                        " cover_photo FROM Movies "
                        f'WHERE Title="{title}" LIMIT 1',
                    )
                    try:
                        year, category, distribution, description, url, cover_photo = (
                            cursor.fetchone()
                        )
                        new_movie = Movie(
                            title=title,
                            year=year,
                            distribution=distribution,
                            description=description,
                            url=url,
                            cover_photo=cover_photo,
                            category=category_map[category],
                            genres=genres,
                        )
                        session.add(new_movie)
                    except Exception as e:
                        logging.error(
                            f"While handling '{title}' - {get_exception_string(e)}"
                        )
            logging.info("Committing the changes")
            cursor.close()
            session.commit()


class Utils:
    """Contains methods for performing various common tasks"""

    @staticmethod
    @click.command()
    @click.argument("Directory", type=click.Path(exists=True, file_okay=False))
    @click.option(
        "-o",
        "--output",
        type=click.Path(dir_okay=False),
        help="Filename under which to save the data",
        default="movies-data.db",
    )
    @click.option(
        "-p",
        "--pattern",
        help="Pattern for the .csv filename",
        default="*",
    )
    def create_db(directory, output, pattern):
        """Save all the movie data to a sqlite3 database under movies table"""
        import sqlite3

        csv_filenames = glob.glob(os.path.join(directory, pattern + ".csv"))
        assert (
            csv_filenames
        ), f"Zero files matched the pattern '{pattern}' in the directory '{directory}'"
        conn = sqlite3.connect(output)
        for csv_file in csv_filenames:
            df = pandas.read_csv(csv_file)
            logging.info("Handling %d movie data from %s" % (len(df), csv_file))
            df.to_sql(name="Movies", con=conn, if_exists="append")
        cursor = conn.cursor()
        cursor.execute("select count(title) from movies")
        logging.info(f"Total entries in the table movies - {cursor.fetchone()[0]}")

    @staticmethod
    @click.command()
    @click.argument("Directory", type=click.Path(exists=True, file_okay=False))
    @click.option(
        "-f",
        "--formats",
        multiple=True,
        help="Targeted export format - csv",
        default=["csv"],
        type=click.Choice(["json", "excel", "html", "pickle", "markdown", "csv"]),
    )
    @click.option(
        "-o",
        "--output",
        type=click.Path(dir_okay=False),
        help="Filename under which to save the data",
        default="movies-data",
    )
    @click.option(
        "-p",
        "--pattern",
        help="Pattern for the .csv filename",
        default="*",
    )
    def to_format(directory, formats, output, pattern):
        """Export contents of .csv file to various formats"""
        csv_filenames = glob.glob(os.path.join(directory, pattern + ".csv"))
        assert (
            csv_filenames
        ), f"Zero files matched the pattern '{pattern}' in the directory '{directory}'"
        format_info = {
            "csv": {"write_mode": "w", "function": "to_csv", "extension": "csv"},
            "json": {"write_mode": "w", "function": "to_json", "extension": "json"},
            "excel": {"write_mode": "wb", "function": "to_excel", "extension": "xlsx"},
            "html": {"write_mode": "w", "function": "to_html", "extension": "html"},
            "pickle": {"write_mode": "wb", "function": "to_pickle", "extension": "pkl"},
            "markdown": {
                "write_mode": "w",
                "function": "to_markdown",
                "extension": "md",
            },
        }
        for format in formats:
            format_details = format_info[format]
            saved_to = output + "." + format_details["extension"]
            df_list = []
            for csv_file in csv_filenames:
                df = pandas.read_csv(csv_file)
                df_list.append(df)
                logging.info("Handling %d movie data from %s" % (len(df), csv_file))
            new_df = pandas.concat(df_list)
            with open(saved_to, format_details["write_mode"]) as fh:
                handler_func = getattr(new_df, format_details["function"])
                handler_func(fh)

            logging.info(f"Movies data (%s) saved to %s" % (format, saved_to))


def entry_point():
    data_hunter.add_command(Utils.create_db)
    data_hunter.add_command(Utils.to_format)
    data_hunter.add_command(DatabaseRelater.relate_tables)

    # fire up
    try:
        data_hunter()
    except Exception as e:
        logging.error("Msg - " + get_exception_string(e))


if __name__ == "__main__":
    entry_point()
