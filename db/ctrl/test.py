import sys
sys.path.append('..')
import table_cr as db
from sqlalchemy import  create_engine
from sqlalchemy.orm import sessionmaker
def getSession(): 
    engine = create_engine('sqlite:////home/chunwei/swin2/db/database.db', echo=False)
    # create a Session
    Session = sessionmaker(bind=engine)
    session = Session()  
    return session

def showReplys():
    se = getSession()
    u = se.query(db.User).filter(db.User.id == 1).first()
    replys = u.replys
    for r in replys:
        print r.replyto, r.status

def showMessages():
    se = getSession()
    u = se.query(db.User).filter(db.User.id == 1).first()
    messages = u.messages
    print messages
    for m in messages:
        print m
        print m.status
        print m.message.title
        print m.message.item.content
    
def showUsers():
    se = getSession()
    us = se.query(db.User).all()
    for u in us:
        print u.name
        print u.pwd

if __name__ == '__main__':
    showUsers()
    showMessages()
   
