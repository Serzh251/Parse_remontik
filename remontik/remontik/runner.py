from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from remontik import settings
from remontik.spiders.remontikspider import RemontikspiderSpider


if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(RemontikspiderSpider)
    process.start()
