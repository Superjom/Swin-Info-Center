import sys
sys.path.append('../../')
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http.request import Request
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from swin.items import SwinItem

class SwinSpider(CrawlSpider):
    name = "swin"
    allowed_domains = [
        "pkusz.edu.cn",
        "news.pkusz.edu.cn",
    ]

    start_urls = [
        "http://www.pkusz.edu.cn/",
        "http://news.pkusz.edu.cn/",
    ]

    rules = (
        #only extract links here
        Rule(SgmlLinkExtractor(allow=r'http://www.pkusz.edu.cn')),
        #extract content here
        Rule(SgmlLinkExtractor(allow=r'http://news.pkusz.edu.cn/index.php?m=content&c=index\.*'),callback="parse"),
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
        urls = hxs.select('//div[contains(@class,"f_title")]/a[contains(@href,"news.pkusz.edu.cn")]/@href').extract()
        self.start_urls.extend(urls)
        
        for url in urls:
            yield Request(url, self.parse)
        #extract data
        item = SwinItem()
        title = hxs.select('//div[contains(@class,"titlelb2")]/b/text()').extract()
        if title: 
            item['title'] = title[0]
        content = hxs.select('//div[contains(@id,"content")]').extract()
        if content:
            item['content'] = content[0]
        yield item

