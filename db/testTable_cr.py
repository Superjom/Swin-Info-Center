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
            "./logo_url",
        )  
        session = self.getSession()
        print 'get users'
        users = session.query(db.User)
        print [u.name for u in users]
        session.add(user)
        session.commit()


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
        circle = db.Circle(
            "circle1",
            "./circle/logo",
            "the des",
        )
        self.commit(circle)
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
            "the creator",
            0,
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
        r = db.Reply(dt.datetime.today(), 0, 'replyto <>')
        item = db.ReplyItem('reply content')
        session.add_all([r, item])
        session.commit()
    
    @deco
    def testCircleAddUser(self):
        print '.. search circle'
        session = self.getSession()
        c = session.query(db.Circle).first()
        u = session.query(db.User).first()
        c.users.append(u)
        session.add_all([c,u])
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
        

    def commit(self, ob):
        session = self.getSession()
        session.add(ob)
        session.commit()
    
if __name__ == '__main__':
    testbase = TestDatabase()
    testbase.testAddUser()
    testbase.testAddTagKind()
    t = testbase
    t.testAddTag()
    t.testAddCircleKind()
    t.testAddCircle()
    t.testCircleKindAppendCircle()
    t.testAddMessage()
    t.testPushMessage()
    t.testAddFollower()
    t.testAddReply()
    t.testCircleAddUser()
    t.testUserAddTag()
    
    
