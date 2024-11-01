#!/usr/bin/python3

import click
import os
import pandas
import glob


@click.group()
def data_hunter():
    """Manipulate .csv data generated accordingly"""


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
            click.secho(
                "> Handling %d movie data from %s" % (len(df), csv_file), color="yellow"
            )
            df.to_sql(name="Movies", con=conn, if_exists="append")
        cursor = conn.cursor()
        cursor.execute("select count(title) from movies")
        click.secho(
            f"> Total entries in the table movies - {cursor.fetchone()[0]}",
            color="green",
        )

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
                click.secho(
                    "> Handling %d movie data from %s" % (len(df), csv_file),
                    color="yellow",
                )
            new_df = pandas.concat(df_list)
            with open(saved_to, format_details["write_mode"]) as fh:
                handler_func = getattr(new_df, format_details["function"])
                handler_func(fh)

            click.secho(
                f"> Movies data (%s) saved to %s" % (format, saved_to),
                color="cyan",
            )


def entry_point():
    data_hunter.add_command(Utils.create_db)
    data_hunter.add_command(Utils.to_format)
    data_hunter()


if __name__ == "__main__":
    entry_point()
