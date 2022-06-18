import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose, Join, SelectJmes


class RemontikItem(scrapy.Item):
    _id = scrapy.Field()
    category_name = scrapy.Field(output_processor=TakeFirst())
    work_name = scrapy.Field(output_processor=TakeFirst())
    work_price = scrapy.Field()
    category_link = scrapy.Field(output_processor=TakeFirst())

