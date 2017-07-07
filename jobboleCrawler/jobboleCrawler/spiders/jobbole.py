# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse

from scrapy.loader import ItemLoader
from jobboleCrawler.items import JobbolecrawlerItem
from jobboleCrawler.utils.common import get_md5

class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):

        post_nodes = response.css("#archive > .post.floated-thumb > .post-thumb > a");
        for post_node in post_nodes:
            img_url = post_node.css("img::attr(href)").extract_first("");
            post_url = post_node.css("::attr(href)").extract_first("");
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.parseDetail)


    def parse_detail(self, response):


        # load Itemloader
        item_loader = ItemLoader(item=JobbolecrawlerItem(), response=response)
        item_loader.add_css('title', 'div.entry-header > h1::text')
        item_loader.add_value('url', response.url)


        pass

