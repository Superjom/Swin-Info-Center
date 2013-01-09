# -*- coding: utf-8 -*
'''
Created on Jan 9, 2013

@author: chunwei
'''
# -*- coding: utf-8 -*
'''
Created on 2012-12-20

@author: superjom
'''

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import table_cr as db
from sqlalchemy import  create_engine, and_, or_
from sqlalchemy.orm import sessionmaker
from ctrl.common import getSession
import datetime


def addNews(station_name, title, content):
    session = getSession()

    station = session.query(db.Station).filter(db.Station.name == station_name).first()
    date = datetime.datetime.today()
    news = db.News(title, date)
    news.item = db.NewsItem(content)
    station.news.append(news)
    session.add(news)
    session.add(station)
    print ">> Succeed add news: <<%s>>" % title
    users = station.users
    for u in users:
        u.news.append(news)
        session.add(u)
    session.commit()


if __name__ == '__main__':
    addNews(u'深圳研究生院官网', 'hello the news', 'the content of news')
    
    
    
    
    
    
    
    
    
    

