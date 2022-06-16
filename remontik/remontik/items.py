import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose, Join


class RemontikItem(scrapy.Item):
    _id = scrapy.Field()
    article_author = scrapy.Field(output_processor=TakeFirst())
    article_urls = scrapy.Field(output_processor=TakeFirst())
    article_name = scrapy.Field(output_processor=TakeFirst())
    article_image = scrapy.Field()
    article_tag = scrapy.Field()
    article_add_datetime = scrapy.Field(output_processor=TakeFirst())
