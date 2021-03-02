# SCRAPY CRAWLERS
A project using scrapy to crawl the address of Aldi's and Leclerc's stores.

## INSTALLATION

### Python
Download and install python3.9 from https://www.python.org/downloads/.

In the root folder run:
```
sudo apt-get install libmysqlclient-dev
pip install -r requirements.txt
```

## USAGE

In root folder:

### All spiders
```
python3 run.py
```

### One spider
```
scrapy crawl <spider>
```

### Arguments
- `-c`, `--csv` : Export to a csv file
- `-p`, `--print` : Print results
- `-s`, `--spiders` : conccurent spiders (default: 2)

### Environnement variables
- `CONNECTION` : MySQL database connection string 
