# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

def serialize_text(value):
    #return value
    print value.encode('utf-8')
    try:
        ret = value.encode('utf-8')
    except:
        ret = value

    return ret

class CurationSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    article_id = scrapy.Field()
    title = scrapy.Field()
    category_list = scrapy.Field()
    update_date = scrapy.Field()
    author = scrapy.Field()
    page_view = scrapy.Field()
    fav_count = scrapy.Field()
    contents = scrapy.Field()
    full_page = scrapy.Field()
    source_links = scrapy.Field()
    source_twitter_links = scrapy.Field()




