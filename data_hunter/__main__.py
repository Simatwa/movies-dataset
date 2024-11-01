import argparse
import os
import data_hunter
from fzmovies_api.filters import MovieGenreFilter

parser = argparse.ArgumentParser(
    prog="data-hunter",
    description=data_hunter.__info__,
    epilog="There's no gurantee that the data generated are correct.",
)
parser.add_argument(
    "-g",
    "--genres",
    nargs="*",
    choices=list(MovieGenreFilter.available_genres) + ["_"],
    metavar=f"[{'|'.join(MovieGenreFilter.available_genres)}]",
    help="Movie genres - %(default)s",
    default=["_"],
)
parser.add_argument(
    "-c",
    "--categories",
    nargs="*",
    default=["_"],
    choices=["Hollywood", "Bollywood", "_"],
    metavar="[Bollywood|Bollywood|_]",
    help="Movie category - %(default)s",
)
parser.add_argument(
    "-l",
    "--limit",
    type=int,
    help="Total movies per genre(multiple of 20) - %(default)d",
    default=1_000_000,
)
parser.add_argument(
    "-d",
    "--dir",
    help="Parent directory to save the datasets to - %(default)s",
    default=os.getcwd(),
)
parser.add_argument(
    "-p",
    "--prefix",
    help="Datasets filename prefix - %(default)s",
    default="",
)
parser.add_argument(
    "-q",
    "--quiet",
    action="store_true",
    help="Do not stdout any informative texts - %(default)s",
)
parser.add_argument(
    "-w",
    "--overwrite",
    action="store_true",
    help="Clear all $prefix*.csv file in the $dir - %(default)s",
)
parser.add_argument(
    "-t",
    "--trace",
    action="store_true",
    help="Maintain trace of the hunting progress - %(default)s",
)
parser.add_argument(
    "-v", "--version", action="version", version=f"%(prog)s v{data_hunter.__version__}"
)
args = parser.parse_args()


def main():
    hunter = data_hunter.MovieDataHunter(genres=args.genres, categories=args.categories)
    try:
        if args.overwrite:
            import glob

            for file in glob.glob(os.path.join(args.dir, args.prefix + "*.csv")):
                os.remove(file)
        total_movies = 0
        for category, genre, movies_count, newly_saved_amount, saved_to in hunter.hunt(
            dir=args.dir,
            prefix=args.prefix,
            limit=args.limit,
            stream=True,
        ):
            total_movies += newly_saved_amount
            if not args.quiet:
                print(
                    "> [Category : %s] - [Genre : %s] - [ Movies : %d] - [Total : %d]"
                    % (category, genre, movies_count, total_movies),
                    end="\n" if args.trace else "\r",
                )
    except Exception as e:
        print(
            "Error : " + e.args[1] if e.args and len(e.args) > 1 else str(e),
            "Quitting!",
            sep="\n",
        )
        from sys import exit

        exit(1)


if __name__ == "__main__":
    main()
