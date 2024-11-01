<h1 align="center"> movies-dataset </h1>
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