# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import math
import requests
import scrapy

from stores.spiders.base_spider import BaseSpider
from stores.items import StoresItem


class AldiSpider(BaseSpider):
    name = 'aldi'
    url = 'https://www.yellowmap.de/partners/AldiNord/Html/Poi.aspx?SessionGuid={}&View=4&ClearGroups=MapNav,GeoMap&Page={}&ClearParas=PoiListPageSize&Step='
    store_per_page = 5
    session = 'effc178a-0801-445b-9912-99e48144765f' #To update


    def start_requests(self):

        url = self.url.format(session, 1)
        request = requests.get(url)

        parser = BeautifulSoup(request.text, 'html.parser')
        elem = parser.select_one('div.PoiListBrowseControlUp strong')
        page_count = math.ceil(int(elem.text) / self.store_per_page)
        self.init_progress_bar(page_count - 1)

        response = scrapy.http.TextResponse(url, body=request.text.encode())
        self.parse(response)

        for i in range(2, page_count + 1):
            r = scrapy.Request(
                url=self.url.format(session, i),
                callback=self.parse,
                dont_filter=True,
            )

            yield r


    def get_results(self, response, store_sel):
        name_sel = './/p[@class="PoiListItemTitle"]/text()'
        address_sel = './/address/text()'
        city_sel = './/address/text()[2]'

        results = []
        result = StoresItem()
        stores = response.xpath(store_sel)
        for store in stores:
            city = store.xpath(city_sel).extract_first()

            result['name'] = store.xpath(name_sel).extract_first()
            result['address'] = store.xpath(address_sel).extract_first()
            result['zipcode'] = city.split()[0]
            result['city'] = city.split(' ', 1)[1].strip()

            results.append(result.copy())

        return results


    def parse_store(self, response):
        store_sel1 = '//tr[@class="ItemTemplate"]'
        store_sel2 = '//tr[@class="AlternatingItemTemplate"]'

        results = self.get_results(response, store_sel1)
        results += self.get_results(response, store_sel2)

        return results
