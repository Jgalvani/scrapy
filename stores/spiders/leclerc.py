# -*- coding: utf-8 -*-
import json
import requests
import scrapy

from stores.spiders.base_spider import BaseSpider
from stores.items import StoresItem


class StoresSpider(scrapy.Spider):
    name = 'leclerc'
    headers = { 'referer': 'https://www.e.leclerc/' }
    url = 'https://api.woosmap.com/stores/search?key=woos-6256d36f-af9b-3b64-a84f-22b2342121ba&lat=46.710873&lng=2.181086&stores_by_page=100&limit=100&page={}&query=user.type%3A%3D%22pdv%22%20AND%20user.commercialActivity.activityCode%3A%3D%22101%22%20OR%20user.commercialActivity.activityCode%3A%3D%22102%22'


    def start_requests(self):

        url = self.url.format(1)
        request = requests.get(url, headers=self.headers)
        response = scrapy.http.TextResponse(url, body=request.text.encode())
        self.parse(response)

        data = request.json()
        page_count = int(data['pagination']['pageCount'])

        for i in range(2, page_count):
            r = scrapy.Request(
                url=self.url.format(i),
                callback=self.parse,
                dont_filter=True,
                headers=self.headers
            )

            yield r


    def parse_store(self, response):
        results = []
        result = StoresItem()
        data = json.loads(response.body)

        for feature in data['features']:
            properties = feature['properties']

            result['name'] = properties['name']
            result['address'] = ' - '.join(properties['address']['lines'])
            result['city'] = properties['address']['city']
            result['zipcode'] = properties['address']['zipcode']

            results.append(result.copy())

        return results

