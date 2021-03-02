# SCRAPY CRAWLERS
A project using scrapy to crawl the address of Aldi's and Leclerc's stores.

## INSTALLATION

### Python
Download and install python3.9 from https://www.python.org/downloads/.

In root folder run:
```
sudo apt-get install libmysqlclient-dev
pip install -r requirements.txt
```

## USAGE
In root folder:
```
python3 run.py
```

### Arguments
- `-c`, `--csv` : Export to a csv file.
- `-p`, `--print` : Print results.
- `-s`, `--spiders` : conccurent spiders (default: 2).

### One spider
In root folder:
```
scrapy crawl <spider>
```

### Environnement variables
- `CONNECTION` : MySQL database connection string.
