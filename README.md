<h1 align="center"> Movies-Dataset </h1>

<p align="center">
<a href="LICENSE.md"><img src="https://img.shields.io/badge/license-MIT-blue.svg"></a>
<img src="https://img.shields.io/github/repo-size/Simatwa/movies-dataset"></img>
<a href="https://hits.seeyoufarm.com"><img src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com/Simatwa/movies-dataset&count_bg=skyblue"/></a>
</p>
A collection of movies dataset for your ML project or any other task.

You can access the datasets from [/data](/data) in csv format.

Alternatively you can generate your own using the procedures given below.

# Installation

- Ensure you have [Python3.10+](https://python.org) installed.

1. Clone 
   ```sh
   git clone https://github.com/Simatwa/movies-dataset.git
   cd movies-dataset
   ```

2. Install requirements
   ```sh
   pip install -r requirements.txt
   ```

# Usage

Running `python -m data_hunter` will retrieve data from the two categories available *(Hollywood, Bollywood)* across all genres available i.e *(Action, Adventure, Animation, Biography, Comedy, Crime, Documentary, Drama, Family, Fantasy, Film-Noir, History, Horror, Music, Musical, Mystery, Romance, Sci-Fi, Sport, Thriller, War, Western)*

You can pass other options such as `limit`, `dir` etc so as to meet your specific needs.

<details>

<summary>
For more usage info you can run <code>$ python -m data_hunter --help</code>
</summary>

```
usage: data-hunter [-h]
                   [-g [[Action|Adventure|Animation|Biography|Comedy|Crime|Documentary|Drama|Family|Fantasy|Film-Noir|History|Horror|Music|Musical|Mystery|Romance|Sci-Fi|Sport|Thriller|War|Western] ...]]
                   [-c [[Bollywood|Bollywood|_] ...]] [-l LIMIT]
                   [-d DIR] [-p PREFIX] [-q] [-w] [-t] [-v]

A collection of movies dataset for your ML project or any other
task.

options:
  -h, --help            show this help message and exit
  -g, --genres [[Action|Adventure|Animation|Biography|Comedy|Crime|Documentary|Drama|Family|Fantasy|Film-Noir|History|Horror|Music|Musical|Mystery|Romance|Sci-Fi|Sport|Thriller|War|Western] ...]
                        Movie genres - ['_']
  -c, --categories [[Bollywood|Bollywood|_] ...]
                        Movie category - ['_']
  -l, --limit LIMIT     Total movies per genre(multiple of 20) -
                        1000000
  -d, --dir DIR         Parent directory to save the datasets to -
                        /home/smartwa/git/smartwa/movies-dataset
  -p, --prefix PREFIX   Datasets filename prefix -
  -q, --quiet           Do not stdout any informative texts - False
  -w, --overwrite       Clear all $prefix*.csv file in the $dir -
                        False
  -t, --trace           Maintain trace of the hunting progress -
                        False
  -v, --version         show program's version number and exit

There's no gurantee that the data generated are correct.
```

</details>

# Direct Links

| No. | Genre | Link |
|-----|-------|------|
| 1   | Action | ```https://raw.githubusercontent.com/Simatwa/movies-dataset/main/data/action.csv``` |
| 2   | Adventure | ```https://raw.githubusercontent.com/Simatwa/movies-dataset/main/data/adventure.csv``` |
| 3   | Animation | ```https://raw.githubusercontent.com/Simatwa/movies-dataset/main/data/animation.csv``` |
| 4   | Biography | ```https://raw.githubusercontent.com/Simatwa/movies-dataset/main/data/biography.csv``` |
| 5   | Comedy | ```https://raw.githubusercontent.com/Simatwa/movies-dataset/main/data/comedy.csv``` |
| 6   | Crime | ```https://raw.githubusercontent.com/Simatwa/movies-dataset/main/data/crime.csv``` |
| 7   | Documentary | ```https://raw.githubusercontent.com/Simatwa/movies-dataset/main/data/documentary.csv``` |
| 8   | Drama | ```https://raw.githubusercontent.com/Simatwa/movies-dataset/main/data/drama.csv``` |
| 9   | Family | ```https://raw.githubusercontent.com/Simatwa/movies-dataset/main/data/family.csv``` |
| 10   | Fantasy | ```https://raw.githubusercontent.com/Simatwa/movies-dataset/main/data/fantasy.csv``` |
| 11   | Film-Noir | ```https://raw.githubusercontent.com/Simatwa/movies-dataset/main/data/film-noir.csv``` |
| 12   | History | ```https://raw.githubusercontent.com/Simatwa/movies-dataset/main/data/history.csv``` |
| 13   | Horror | ```https://raw.githubusercontent.com/Simatwa/movies-dataset/main/data/horror.csv``` |
| 14   | Music | ```https://raw.githubusercontent.com/Simatwa/movies-dataset/main/data/music.csv``` |
| 15   | Musical | ```https://raw.githubusercontent.com/Simatwa/movies-dataset/main/data/musical.csv``` |
| 16   | Mystery | ```https://raw.githubusercontent.com/Simatwa/movies-dataset/main/data/mystery.csv``` |
| 17   | Romance | ```https://raw.githubusercontent.com/Simatwa/movies-dataset/main/data/romance.csv``` |
| 18   | Sci-Fi | ```https://raw.githubusercontent.com/Simatwa/movies-dataset/main/data/sci-fi.csv``` |
| 19   | Sport | ```https://raw.githubusercontent.com/Simatwa/movies-dataset/main/data/sport.csv``` |
| 20   | Thriller | ```https://raw.githubusercontent.com/Simatwa/movies-dataset/main/data/thriller.csv``` |
| 21   | War | ```https://raw.githubusercontent.com/Simatwa/movies-dataset/main/data/war.csv``` |
| 22   | Western | ```https://raw.githubusercontent.com/Simatwa/movies-dataset/main/data/western.csv``` |

# Combined Datasets Link

| No. | Identity | Link |
|-----|-------|------|
| 1   | Combined `csv` | ```https://raw.githubusercontent.com/Simatwa/movies-dataset/main/data/combined.csv``` |
| 2   | Sqlite3 Database | ```https://raw.githubusercontent.com/Simatwa/movies-dataset/main/data/combined.db``` |

# Further details

In order to make work easier, there's [cli](cli.py) that comes handy in manipulating the data. This is just but not limited to converting them to various formats and even piling them into one sqlite3 database.

