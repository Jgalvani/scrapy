# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class StoresPipeline:

    def process_item(self, row, spider):

        table = os.environ["TABLE"]

        if not row['results']:
            row['results'] == []

        #MYSQL
        #errors = bigquery_client.insert_rows_json(table, [item])

        #if errors:
        #    print(item)
        #    print("errors: " + str(errors))

        if spider.settings['PRINT']:
            print(item)

        return item

