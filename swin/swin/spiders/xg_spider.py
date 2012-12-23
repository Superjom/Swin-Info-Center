# -*- coding: utf-8 -*
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('../../')
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http.request import Request
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from swin.items import SwinItem

class SwinSpider(CrawlSpider):
    name = "xg"
    allowed_domains = [
        "ece.pku.edu.cn",
    ]

    start_urls = [
        "http://www.ece.pku.edu.cn/",
    ]

    rules = (
        #only extract links here
        Rule(SgmlLinkExtractor(allow=r'http://ece.pku.edu.cn')),
        #extract content here
        Rule(SgmlLinkExtractor(allow=r'http://www.ece.pku.edu.cn/index.php?m=content&c=index&a=show&catid=502\.*'),callback="parse"),
    )

    def parse(self, response):
        '''
        extract
        title
        content
        url
        '''
        print '>'*50
        print 'response url: ', response.url
        hxs = HtmlXPathSelector(response)
        print '>>>> repsonse.url: ', response.url
        #get urls
        box = hxs.select('//div[contains(@class,"first")]')
        if box:
            urls = box.select('//li/a[contains(@href,"http://www.ece.pku.edu.cn/index.php?m=content&c=index&a=show&catid=502")]/@href').extract()
        #urls = hxs.select('//div[contains(@class,"f_title")]/a[contains(@href,"news.pkusz.edu.cn")]/@href').extract()
            for url in urls:
                yield Request(url, self.parse)
        #extract data
        item = SwinItem()
        title = hxs.select('//div[contains(@class,"article")]/h1/text()').extract()
        if title: 
            item['title'] = title[0]
        content = hxs.select('//div[contains(@class,"content")]').extract()
        if content:
            item['content'] = content[0]
            item['station'] = u'信息工程学院'
        yield item

