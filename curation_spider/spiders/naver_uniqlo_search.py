# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from curation_spider.spiders.naver_fashion import NaverFashionSpider
import re

from curation_spider.items import CurationSpiderItem

global current_article_id

def custom_process_value(value):
    global current_article_id
    odai_url = 'http://matome.naver.jp/odai/'

    is_first_page = re.search(odai_url + "\d+$", value)

    # これに引っかかるのは、最初のページ'/'をクロールしたあとなので、current_article_idが必ずある
    m = re.search("(http://matome.naver.jp/odai/)goPage\((\d+)\)", value)

    if m:
        url = odai_url + current_article_id + '?page=' + m.group(2)
        ret = url

    elif is_first_page:
        # パージの表記がURLに入っていない場合は「page=1」を追加
        ret = value + '?page=1'

    else:
        ret = value

    return ret


#class NaverUniqloSearchSpider(CrawlSpider):
class NaverUniqloSearchSpider(NaverFashionSpider):
    name = 'naver-uniqlo-search'
    allowed_domains = ['matome.naver.jp']

    # ユニクロで検索して時系列で表示
    base_url = 'http://matome.naver.jp/search?q=%E3%83%A6%E3%83%8B%E3%82%AF%E3%83%AD&sort=ud'
    # MdPagination04の最後の値まで
    page_end_num = 1
    page_range = range(1,page_end_num+1)
    # Naverまとめはページ送りのリンクがJavascriptになっているため、ページのリンクを自分で生成する必要あり
    start_urls = [base_url + '&page=' + str(x) for x in page_range]
    print start_urls
    rules = (
        Rule(LinkExtractor(allow=(r'^http://matome.naver.jp/odai/\d+.*',),
                           restrict_xpaths=('//ul[@class="MdMTMTtlList03"]','//div[@class="MdPagination03"]'),
                           process_value=custom_process_value,
                           ),
             callback='parse_item',
             follow=True
        ),
        # Page送り取得
        Rule(LinkExtractor(allow=(r'^#$',),
                           restrict_xpaths=('//div[@class="MdPagination03"]'),
                           attrs=('href','onclick',),
                           process_value=custom_process_value
                           ),
             callback='parse_item',
             follow=True
        ),
        # URL変換後のものに引っ掛けるルール
        Rule(LinkExtractor(allow=(r'^http://matome.naver.jp/odai/\d+\?page=\d+',),
                           restrict_xpaths=('//div[@class="MdPagination03"]',),
                           process_value=custom_process_value,
                           attrs=('href','onclick'),
                           ),
             callback='parse_item',
             follow=True
        ),
    )


    def parse_item(self, response):
        global current_article_id
        current_url = response.url
        m = re.search('http://matome.naver.jp/odai/(\d+)\?page=\d+', current_url)
        if m:
            current_article_id = m.group(1)
        else:
            raise

        i = CurationSpiderItem()
        return self._extract_fields(i, response, current_article_id)




