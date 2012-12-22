# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

import sys
sys.path.append('../../../')
import db.add_data as add_data
from scrapy.exceptions import DropItem

class SwinPipeline(object):
    def process_item(self, item, spider):
        if item.has_key('content'):
            print '@'*50
            print '>title: ', item['title']
            #add data to sqlite database
            add_data.addNews(item['station'], item['title'], item['content'])
            return item
        else:
            raise DropItem('Error, no content')
        
