# -*- coding: utf-8 -*-
import scrapy


class NaverSpider(scrapy.spiders.SitemapSpider):
    name = "naver"
    allowed_domains = ["matome.naver.jp"]
    sitemap_urls = (
        'http://matome.naver.jp/robots.txt',
        'http://matome.naver.jp/sitemap_matome_A_hot.xml'
    )


    def parse(self, response):
        yield {
            # title要素の文字列を取得する
            'title': response.xpath('///title/text()').extract_first(),
        }