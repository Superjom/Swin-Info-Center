# -*- coding: utf-8 -*
import random 
import unittest
from sqlalchemy import  create_engine
from sqlalchemy.orm import sessionmaker
import table_cr as db
import datetime as dt

def deco(func):
    print '.. > ', func
    return func

class TestDatabase:
    
    def getSession(self): 
        engine = create_engine('sqlite:////home/chunwei/swin2/db/database.db', echo=False)
        # create a Session
        Session = sessionmaker(bind=engine)
        session = Session()  
        return session
    @deco
    def testAddUser(self):
        print '>> add user'
        user = db.User(
            "superjom",
            "511541",
            "superjom@gmail.com",
            "Shenzhen, Guangdong",
            "PKU",
            1.0,
            "static/images/logo_male.jpg",
        )  

        user1 = db.User(
            "shasha",
            "511541",
            "shasha@gmail.com",
            "Beijing",
            "PKU",
            1.0,
            "static/images/logo_female.jpg",
        )  

        user2 = db.User(
            "chunwei",
            "511541",
            "shasha@gmail.com",
            "Beijing",
            "PKU",
            1.0,
            "static/images/logo_female.jpg",
        )  
        session = self.getSession()
        print 'get users'
        session.add_all([user, user1, user2])
        session.commit()
        users = session.query(db.User)
        print [u.name for u in users]


    @deco
    def testAddTagKind(self):
        print '>> add tagkind'
        kind = db.TagKind("Sex")
        session = self.getSession()
        session.add(kind)
        session.commit()
    @deco
    def testAddTag(self):
        tag = db.Tag('Male')
        self.commit(tag)
    @deco
    def testTagKindAppendTag(self):
        print '..find tagkind'
        session = self.getSession()
        tagkind = session.query(db.TagKind).first()
        tag = session.query(db.Tag).first()
        tagkind.tagsappend(tag)
        session.add(tag)
        session.add(tagkind)
        print '..commit'
        session.commit()
    @deco
    def testAddCircleKind(self):
        circle = db.CircleKind("School institutes")
        self.commit(circle)
    @deco
    def testAddCircle(self):
        session = self.getSession()
        circle = db.Circle(
            u"教务处",
            "./circle/logo",
            "the des",
        )
        circle1 = db.Circle(
            u"研究生院",
            "./circle/logo",
            "the des",
        )
        circle2 = db.Circle(
            u"信息协会交流群",
            "./circle/logo",
            "the des",
        )
        session.add_all([circle, circle1, circle2])
        session.commit()
    @deco
    def testCircleKindAppendCircle(self):
        print '..find circlekind'
        session = self.getSession()
        circlekind = session.query(db.CircleKind).first()
        circle = session.query(db.Circle).first()
        circlekind.circles.append(circle)
        session.add(circle)
        session.add(circlekind)
        session.commit()

    @deco
    def testAddMessage(self):
        print 'create message'
        message = db.Message(
            "the title",
            "the summary",
            1,
            dt.datetime.today()
        )
        print 'create messageitem'
        item = db.MessageItem(
            "the content"
        )
        session = self.getSession()
        message.item = item
        session.add_all([message, item])
        session.commit()
    @deco
    def testPushMessage(self):
        print 'search message'
        session = self.getSession()
        message = session.query(db.Message).first()
        print 'push'
        messagemeta = db.MessageMeta(message) 
        session.add_all([message, messagemeta])  
        print 'commit'
        session.commit()

    @deco
    def testAddFollower(self):
        print 'search message'
        session = self.getSession()
        m = session.query(db.Message).first()
        print 'create follower'
        f = db.Follower('superjom', dt.datetime.today())
        m.followers.append(f)
        session.add_all([f, m])
        session.commit()
    
    @deco
    def testAddReply(self):
        print 'add reply'
        session = self.getSession()
        r = db.Reply(dt.datetime.today(), 0, 'replyto <>', 1)
        item = db.ReplyItem('reply content')
        session.add_all([r, item])
        session.commit()
    
    @deco
    def testCircleAddUser(self):
        print '.. search circle'
        session = self.getSession()
        c = session.query(db.Circle).all()
        users = session.query(db.User).all()
        for s in c:
            for u in users:
                s.users.append(u)
                session.add_all([u, s])
        session.commit()

    @deco
    def testUserAddTag(self):
        print '.. search tag'
        session = self.getSession()
        c = session.query(db.Tag).first()
        u = session.query(db.User).first()
        c.users.append(u)
        session.add_all([c,u])
        session.commit()

    @deco
    def testAddNews(self):
        print 'add news'
        session = self.getSession()
        station = session.query(db.Station).first()
        u = session.query(db.User).first()
        for i in range(2):
            news = db.News('the title %d' % i, dt.datetime.today())
            station.news.append(news)
            session.add(news)
        u.stations.append(station)
        session.add_all([station, u])
        session.commit()

    def testAddStations(self):
        session = self.getSession()
        stations = [
            u"深圳研究生院官网",
            u"信息工程学院",
        ]
        for station in stations:
            s = db.Station(station)
            session.add(s)
        session.commit()
        print "add stations OK!"
        

    def commit(self, ob):
        session = self.getSession()
        session.add(ob)
        session.commit()
    
if __name__ == '__main__':
    testbase = TestDatabase()
    t = testbase
    testbase.testAddUser()
    testbase.testAddTagKind()
    t.testAddTag()
    t.testAddCircleKind()
    t.testAddCircle()
    t.testCircleKindAppendCircle()
    #t.testAddMessage()
    #t.testPushMessage()
    #t.testAddFollower()
    #t.testAddReply()
    t.testCircleAddUser()
    t.testUserAddTag()
 
    t.testAddStations()
    #t.testAddNews()
    
