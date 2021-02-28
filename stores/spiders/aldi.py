# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import math
import requests
import scrapy

from stores.spiders.base_spider import BaseSpider
from stores.items import StoresItem


class StoresSpider(scrapy.Spider):
    name = 'aldi'
    url = 'https://www.yellowmap.de/partners/AldiNord/Html/Poi.aspx?SessionGuid=79eddb93-19c2-4b1b-aa05-fbd9501a4f50&View=4&ClearGroups=MapNav,GeoMap&Page={}&ClearParas=PoiListPageSize&Step='
    store_per_page = 5


    def start_requests(self):

        url = self.url.format(1)
        request = requests.get(url)
        response = scrapy.http.TextResponse(url, body=request.text.encode())
        self.parse(response)

        parser = BeautifulSoup(request.text, 'html.parser')
        elem = parser.select_one('div.PoiListBrowseControlUp strong')
        page_count = math.ceil(int(elem.text) / self.store_per_page)

        for i in range(2, page_count):
            r = scrapy.Request(
                url=self.url.format(i),
                callback=self.parse,
                dont_filter=True,
            )

            yield r


    def parse_store(self, response):

        name_sel = './/p[@class="PoiListItemTitle"]/text()'
        address_sel = './/address/text()'
        city_sel = './/address/text()[2]'
        store_sel = '//tr[@class="ItemTemplate"]'
        stores = response.xpath(store_sel)

        results = []
        result = StoresItem()
        for store in stores:
            city = store.xpath(city_sel).extract_first()

            result['name'] = store.xpath(name_sel).extract_first()
            result['address'] = store.xpath(address_sel).extract_first()
            result['zipcode'] = city.split()[0]
            result['city'] = city.split()[1].strip()

            results.append(result.copy())

        return results
