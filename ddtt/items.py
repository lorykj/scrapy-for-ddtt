# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DdttItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    src = scrapy.Field()
    year = scrapy.Field()
    area = scrapy.Field()
    genre = scrapy.Field()
    language = scrapy.Field()
    date = scrapy.Field()
    vote = scrapy.Field()
    vote_cnt = scrapy.Field()
    runtime = scrapy.Field()
    director = scrapy.Field()
    actor = scrapy.Field()
