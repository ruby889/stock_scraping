from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

SPIDER = 'aastocksIndustrySpider'
def run_spider(crawlAll):
    process = CrawlerProcess(get_project_settings())
    process.crawl(SPIDER, crawlAll=crawlAll)
    process.start() # the script will block here until the crawling is finished
    return True
