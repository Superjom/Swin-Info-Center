# -*- coding: utf-8 -*
'''
Created on 2012-12-20

@author: superjom
'''
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import db.ctrl as ctrl
import db.table_def as db
from sqlalchemy import  create_engine, and_, or_
from sqlalchemy.orm import sessionmaker
import datetime


def addNews(station_name, title, content):
    engine = create_engine('sqlite:////home/chunwei/swin2/db/data.db', echo=False)
    # create a Session
    Session = sessionmaker(bind=engine)
    session = Session()

    station = session.query(db.Station).filter(db.Station.name == station_name).first()
    date = datetime.datetime.today()
    news = db.News(date)
    news.item = db.NewsItem(title, content)
    station.news.append(news)
    session.add(news)
    session.add(station)
    session.commit()
    print ">> Succeed add news: <<%s>>" % title
    
    
    
    
    
    
    
    
    
    

