# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from stores.db import insert_rows


class StoresPipeline:

    def get_rows(item):
        """Format item to fit table columns"""
        return [
            [
                item['store'],
                result['name'],
                result['address'],
                result['zipcode'],
                result['city'],
                item['date'],
            ]
            for result in item[results]
        ]

    def process_item(self, item, spider):

        if not item['results']:
            item['results'] == []

        rows = self.get_rows(item)
        insert_rows(rows)

        # Debug
        if item['error']:
            print(item['error'])

        elif spider.settings['PRINT']:
            print(item)

        return item
