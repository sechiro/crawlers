# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from curation_spider.items import CurationSpiderItem
import re

def custom_process_value(value):
    base_url = 'http://mery.jp/'

    is_first_page = re.search(base_url + "\d+$", value)

    if is_first_page:
        # ページの表記がURLに入っていない場合は「page=1」を追加
        ret = value + '?page=1'

    else:
        ret = value

    return ret

class NaverFashionSpider(CrawlSpider):
    name = 'mery-fashion'
    allowed_domains = ['mery.jp']
    #ファッションタグ
    #scrapy crawl mery-fashion -o mery_fashion_category.jl
    base_url = 'http://mery.jp/fashion'

    # Paginationの最後の値まで
    #page_end_num = 680
    page_end_num = 3
    page_range = range(1,page_end_num+1)
    # MERYのファッションカテゴリのページのリンクを生成
    start_urls = [base_url + '?page=' + str(x) for x in page_range]
    print start_urls
    rules = (
        #Rule(LinkExtractor(allow=r'^#'), follow=True),
        Rule(LinkExtractor(allow=(r'^http://mery.jp/\d+',),
                           restrict_xpaths=('//h3[@class="article_list_title"]'),
                           process_value=custom_process_value
                           ),
             callback='parse_item',
             follow=True
        ),
        # Page送り取得
        Rule(LinkExtractor(allow=(r'^\d+$',),
                           restrict_xpaths=('//div[@id="paginate"]'),
                           attrs=('href',),
                           ),
             callback='parse_item',
             follow=True
        ),
        # URL変換後のものに引っ掛けるルール
        Rule(LinkExtractor(allow=(r'^http://mery.jp/\d+.*',),
                           restrict_xpaths=('//div[@id="paginate"]'),
                           attrs=('href',),
                           ),
             callback='parse_item',
             follow=True
        ),
    )


    def parse_item(self, response):
        i = CurationSpiderItem()
        return self._extract_fields(i, response)


    def _extract_fields(self, i, response):
        i['url'] = response.url
        # "?page=xx"が入らないURLを取得
        original_url = response.xpath('//meta[@property="og:url"]/@content').extract_first()
        m = re.match('https?://mery.jp/(\d+).*', original_url)
        if m:
            i['article_id'] = m.group(1)
        else:
            # idを抜き出せなかったら、URLをそのまま入れる
            i['article_id'] = original_url
        i['category_list'] = response.xpath('//ul[@class="clearfix"]/li/a/text()').extract()
        i['title'] = response.xpath('/html/head/title/text()').extract_first()
        i['update_date'] = response.xpath('//p[@class="article_date"]/@content').extract_first()
        i['author'] = response.xpath('//p[@class="side_curator_name"]/a/span/text()').extract_first()
        i['page_view'] = response.xpath('//ul[@class="articleData"]/li[@class="view"]/span/text()').extract_first()
        i['fav_count'] = response.xpath('//ul[@class="articleData"]/li[@class="like"]//span[@class="like_pop"]/text()').extract_first()
        #i['contents'] = response.xpath('//div[@class="LyMain"]//div[@class="mdMTMWidget01Content01 MdCF"]').extract()
        i['full_page'] = response.xpath('/html/body').extract()
        i['source_links'] = list(set(response.xpath('//div[@class="article_content"]//a/@href').extract() ) )

        return i
