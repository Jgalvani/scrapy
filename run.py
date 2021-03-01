import argparse
import datetime

from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor, defer


### SETTINGS
configure_logging()
settings = get_project_settings()

parser = argparse.ArgumentParser()

parser.add_argument("-c", "--csv", help="Export to csv", type=bool, default=False, const=True, nargs='?')
parser.add_argument("-p", "--print", help="Print results", type=bool, default=False, const=True, nargs='?')
parser.add_argument("-s", "--spiders", help="conccurent spiders", type=int, default=2)

args = parser.parse_args()

if args.csv:
    settings['FEED_FORMAT'] = 'csv'
    settings['FEED_URI'] = f'stores_{datetime.date.today()}.csv'

settings['PRINT'] = args.print
settings['CONCCURENT_SPIDERS'] = args.spiders


### RUN SPIDERS
runner = CrawlerRunner(settings)

@defer.inlineCallbacks
def crawl(spider_list, runner):
    crawl_deferred = False
    deferred_list = []

    for spider_name in spider_list:
        spider = runner.spider_loader.load(spider_name)
        deferred_list.append(runner.crawl(spider))

        if len(deferred_list) == settings["CONCURRENT_SPIDERS"]:
            crawl_deferred = True
            yield defer.DeferredList(deferred_list)
            deferred_list = []

    if deferred_list:
        crawl_deferred = True
        yield defer.DeferredList(deferred_list)

    if crawl_deferred:
        reactor.stop()

    return crawl_deferred


if not runner.spider_loader.list():
    raise Warning("Nothing to crawl")

d = defer.maybeDeferred(crawl, runner.spider_loader.list(), runner)
if hasattr(d, "result") and not d.result:
    raise Warning("Nothing to crawl")
else:
    reactor.run()
