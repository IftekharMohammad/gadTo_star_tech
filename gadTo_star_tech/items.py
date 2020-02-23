# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GadtoStarTechItem(scrapy.Item):
    website_name = scrapy.Field()
    parent_catagory_name = scrapy.Field()
    child_catagory_name = scrapy.Field()
    item_name = scrapy.Field()
    brand_name = scrapy.Field()
    price = scrapy.Field()
    image_urls = scrapy.Field()
    description = scrapy.Field()
    specification = scrapy.Field()
