import scrapy
from bs4 import BeautifulSoup
from itemloaders import ItemLoader
from scrapy.http import HtmlResponse
from scrapy.selector import Selector
from remontik.items import RemontikItem


class RemontikspiderSpider(scrapy.Spider):
    name = 'remontikspider'
    allowed_domains = ['remontnik.ru']
    start_urls = ['https://www.remontnik.ru/moskva/']

    def __init__(self, name=None, **kwargs):
        super().__init__(name=None, **kwargs)

    def parse(self, response: HtmlResponse, **kwargs):
        # links = response.css('a.subcat-link::attr(href)').extract()
        #
        # for link in links:
        #     yield response.follow(link, callback=self.parse_item)
        categories_block = response.xpath('//rtk-catalog-category').getall()
        categories_block = categories_block[0:12]
        for _ in range(3):
            categories_block.pop(5)  # отсекаем не нужные категории, далее имеем список нужных категорий

        page = ''.join(categories_block)
        soup = BeautifulSoup(page, 'lxml')
        links = []  # список будет заполнен очищенными и только нужными ссылками
        for link in soup.find_all('a'):
            links.append(link.get('href'))

        for link in links:
            yield response.follow(link, callback=self.parse_work_pages)


    def parse_work_pages(self, response):
        work_links = response.xpath('//tr/td/a/@href').getall()

        for link in work_links:
            yield response.follow(link, callback=self.parse_item)

    def parse_item(self, response):
        selector = Selector(response=response, type='html')
        item_loaded = ItemLoader(item=RemontikItem(), response=response, selector=selector)

        item_loaded.add_xpath('category_name', '//div[@class = "breadcrumbs"]/a[2]/span/text()')
        item_loaded.add_value('category_link', response.url)
        item_loaded.add_xpath('work_name', '//div[@class = "breadcrumbs"]/span/text()')
        item_loaded.add_xpath('work_price', '//span[@class = "price"]/text()')


        yield item_loaded.load_item()
