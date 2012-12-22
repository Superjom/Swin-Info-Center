# Scrapy settings for swin project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'swin'

SPIDER_MODULES = ['swin.spiders']
NEWSPIDER_MODULE = 'swin.spiders'
ITEM_PIPELINES = [
    'swin.pipelines.SwinPipeline'
]

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'swin (+http://www.yourdomain.com)'
