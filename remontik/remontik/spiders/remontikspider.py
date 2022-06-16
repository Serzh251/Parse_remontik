import scrapy
from itemloaders import ItemLoader
from scrapy.http import HtmlResponse
from bs4 import BeautifulSoup
from remontik.items import RemontikItem


class RemontikspiderSpider(scrapy.Spider):
    name = 'remontikspider'
    allowed_domains = ['remontnik.ru']
    start_urls = ['https://www.remontnik.ru//']

    def __init__(self, name=None, **kwargs):
        super().__init__(name=None, **kwargs)
        self.parse_item = None

    def parse(self, response: HtmlResponse, **kwargs):
        categories_block = response.xpath('//div[@class = "container columns-block"]/div/div').getall()
        categories_block = categories_block[0:12]
        for _ in range(3):
            categories_block.pop(5)  # отсекаем не нужные категории, далее имеем список нужных категорий

        page = ''.join(categories_block)
        soup = BeautifulSoup(page)
        links = []  # список будет заполнен очищенными и только нужными ссылками
        for link in soup.find_all('a'):
            links.append(link.get('href'))

        for link in links:
            yield response.follow(link, callback=self.parse_item)

        def parse_item(self, response):
            item_loaded = ItemLoader(item=RemontikItem(), response=response)

            item_loaded.add_xpath('article_author',
                                  '//span[@class = "tm-user-info tm-article-snippet__author"]/a/@title'),
            item_loaded.add_value('article_urls', response.url)
            item_loaded.add_xpath('article_name',
                                  '//h1[@class = "tm-article-snippet__title tm-article-snippet__title_h1"]/span/text()')
            item_loaded.add_xpath('article_image', '//div[@id = "post-content-body"]/div/figure/*/@data-src')
            item_loaded.add_xpath('article_text', '//div[@id="post-content-body"]/div/text()|'
                                                  '//div[@id="post-content-body"]/div/*/text()')
            item_loaded.add_xpath('article_tag',
                                  '//div[@class="tm-article-presenter__meta"]/div[position()=1]/ul/li/a/text()')
            item_loaded.add_xpath('article_hub',
                                  '//div[@class="tm-article-presenter__meta"]/div[position()=2]/ul/li/a/text()')
            item_loaded.add_xpath('article_add_datetime',
                                  '//span[@class="tm-article-snippet__datetime-published"]/time/@title')

            yield item_loaded.load_item()
