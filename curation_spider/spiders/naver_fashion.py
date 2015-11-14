# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from curation_spider.items import CurationSpiderItem
import re

global current_article_id

def custom_process_value(value):
    #global current_url
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

class NaverFashionSpider(CrawlSpider):
    name = 'naver-fashion'
    allowed_domains = ['matome.naver.jp']
    #ファッションタグ
    #base_url = 'http://matome.naver.jp/topic/1Hio8'
    #scrapy crawl naver-fashion -o uniqlo_category.jl
    #ユニクロタグ
    base_url = 'http://matome.naver.jp/topic/1Luw0'

    # MdPagination04の最後の値まで
    page_end_num = 2764
    page_range = range(1,page_end_num+1)
    # Naverまとめはページ送りのリンクがJavascriptになっているため、ページのリンクを自分で生成する必要あり
    start_urls = [base_url + '?page=' + str(x) for x in page_range]
    print start_urls
    rules = (
        #Rule(LinkExtractor(allow=r'^#'), follow=True),
        Rule(LinkExtractor(allow=(r'^http://matome.naver.jp/odai/\d+',),
                           restrict_xpaths=('//ul[@class="MdMTMTtlList02"]'),
                           process_value=custom_process_value
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
        m = re.search('http://matome.naver.jp/odai/(\d+).*', current_url)
        if m:
            current_article_id = m.group(1)
        else:
            raise

        i = CurationSpiderItem()
        return self._extract_fields(i, response, current_article_id)


    def _extract_fields(self, i, response, current_article_id):
        i['url'] = response.url
        i['article_id'] = current_article_id
        i['title'] = response.xpath('/html/head/title/text()').extract_first()
        i['update_date'] = response.xpath('//p[@class="mdHeading01DescDate"]/text()').extract_first()
        i['author'] = response.xpath('//span[@class="mdHeading01UserName"]/a/text()').extract_first()
        i['page_view'] = response.xpath('//span[@class="mdHeading01CountPV"]/span[@class="mdHeading01CountNum"]/text()').extract_first()
        i['fav_count'] = response.xpath('//span[@class="mdHeading01CountFV"]/span[@class="mdHeading01CountNum"]/text()').extract_first()
        i['contents'] = response.xpath('//div[@class="LyMain"]//div[@class="mdMTMWidget01Content01 MdCF"]').extract()
        #i['source_links'] = response.xpath('//div[@class="LyMain"]//a[@class="mdMTMWidget01ItemUrl01Link"]/@href').extract()
        i['source_links'] = list(set(response.xpath('//div[@class="LyMain"]//div[@class="mdMTMWidget01Content01 MdCF"]//a/@href').extract() ) )

        i['source_twitter_links'] = response.xpath('//div[@class="LyMain"]//a[@class="mdMTMWidget01ItemTweetTime"]/@href').extract()
        return i
