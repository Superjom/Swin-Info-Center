# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class SwinItem(Item):
    # define the fields for your item here like:
    # name = Field()
    title = Field()
    content = Field()
    url = Field()
    station = Field()

    def __str__(self):
        return "Get Website: station=%s title=%s content=%d" % (self.get('station'), self.get('title'), len(self.get('content')))
