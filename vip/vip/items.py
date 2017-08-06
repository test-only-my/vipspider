# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# class VipTypeItem(scrapy.Item):
class VipGoodItem(scrapy.Item):
    type_id = scrapy.Field()
    type_name = scrapy.Field()
    type_link = scrapy.Field()
    type_path = scrapy.Field()


# class VipGoodItem(scrapy.Item):
    brand_id = scrapy.Field()
    good_name = scrapy.Field()
    good_price = scrapy.Field()
    good_link = scrapy.Field()


# class VipImgItem(scrapy.Item):
    img_name = scrapy.Field()
    img_url = scrapy.Field()
    img_path = scrapy.Field()
