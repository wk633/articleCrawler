# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse

# from scrapy.loader import ItemLoader
from jobboleCrawler.items import ArticleItemLoader
from jobboleCrawler.items import JobboleArticleItem
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
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse_detail)

    def parse_detail(self, response):

        # load Itemloader
        item_loader = ArticleItemLoader(item=JobboleArticleItem(), response=response)
        item_loader.add_css("title", ".entry-header h1::text")
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_css("create_date", "p.entry-meta-hide-on-mobile::text")
        item_loader.add_css("praise_nums", ".vote-post-up  h10::text")
        item_loader.add_css("fav_nums", ".bookmark-btn::text")
        item_loader.add_css("tag_list", "p.entry-meta-hide-on-mobile a::text")
        item_loader.add_css("content", "div.entry")

        article_item = item_loader.load_item()

        yield article_item

