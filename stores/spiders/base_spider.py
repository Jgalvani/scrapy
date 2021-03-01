import os
from tqdm import tqdm
import scrapy
import time


class BaseSpider(scrapy.Spider):

    #### INIT ####
    def get_spider_position(self, name):
        spider_list = sorted([f for f in os.listdir('stores/spiders') if f.endswith('.py') and f != 'base_spider.py'])

        if f"{name}.py" not in spider_list:
                raise ValueError("Crawler {name} not found")

        return spider_list.index(f"{name}.py") + 1

    def __init__(self):
        self.pos = self.get_spider_position(self.name)

    def init_progress_bar(self, page_count):
        self.pbar = tqdm(total=page_count, desc=f'{self.name} pos={self.pos})')

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(BaseSpider, cls).from_crawler(crawler, *args, **kwargs)

        crawler.signals.connect(spider.item_scraped, signal=scrapy.signals.item_scraped)
        crawler.signals.connect(spider.item_scraped, signal=scrapy.signals.item_dropped)

        return spider

    def item_scraped(self, item, spider):
        self.pbar.update()

    #### PARSE ####
    def parse(self, response):
        results = [] if response.status != 200 else self.parse_store(response)
        item = self.create_item(results, response)

        return item

    def create_item(self, results, response):
        item = {}
        item["store"] = self.name
        item['title'] = response.xpath("//title/text()").extract_first()
        item["url"] = response.url
        item["date"] = time.strftime("%Y-%m-%d")
        item["timestamp"] = int(time.time())
        item['error'] = response.body.decode() if response.status != 200 else None

        #Convert items to dicts
        if results:
            for i, result in enumerate(results):
                results[i] = dict(result)

        item['results'] = results

        return item
