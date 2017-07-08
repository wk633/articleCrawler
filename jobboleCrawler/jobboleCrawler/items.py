# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import re
from scrapy.loader.processors import MapCompose, TakeFirst, Join
import datetime
from scrapy.loader import ItemLoader


class JobbolecrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


# override ItemLoader
class ArticleItemLoader(ItemLoader):
    # custom itemloader
    default_output_processor = TakeFirst()


def date_convert(value):
    try:
        create_date = datetime.datetime.strptime(value, "%Y%m%d").date()
    except Exception as e:
        create_date = datetime.datetime.now().date()
    return create_date


def get_nums(value):
    match_re = re.match(".*?(\d+).*", value);
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0
    return nums

def filter_tag(value):
    if "评论" in value:
        return ""
    else:
        return value

class JobboleArticleItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    create_date = scrapy.Field(
        input_processor=MapCompose(date_convert)
    )
    praise_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    fav_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    tag_list = scrapy.Field(
        input_processor=MapCompose(filter_tag),
        output_processor=Join(", ")
    )
    content = scrapy.Field()
    front_img_url = scrapy.Field()
    front_img_path = scrapy.Field()