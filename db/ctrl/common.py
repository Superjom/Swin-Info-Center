import sys
sys.path.append('..')
#import table_cr as db
from sqlalchemy import  create_engine
from sqlalchemy.orm import sessionmaker

def getSession(): 
    engine = create_engine('sqlite:////home/chunwei/swin2/db/database.db', echo=False)
    # create a Session
    Session = sessionmaker(bind=engine)
    session = Session()  
    return session

def commit(ob):
    session = getSession()
    session.add(ob)
    session.commit()

def commit_all(list):
    session = getSession()
    session.add_all(list)
    session.commit()

class Ctrl:
    def __init__(self, session, ob):
        '''
        joint session
        '''
        self.session = session
        self.cur = None
        self.ob = ob

    def add(self, ob):
        '''
        add new object
        '''
        self.commit(ob)

    def get(self, id):
        return self.session.query(self.ob).filter(self.ob.id == id).first()

    def get_byName(self, session, name):
        return session.query(self.ob).filter(self.ob.name == name).first()

    def setCur(self, id):
        '''
        pass in id
        and get first object
        '''
        self.cur = self.session.query(self.ob).filter(self.ob.id == id).first()

    def show_all(self):
        print '.. show all ', self.ob
        obs = self.session.query(self.ob).all()
        for o in obs:
            print o.name

    def commit(self, ob):
        self.session.add(ob)
        self.session.commit()

    def commit_all(self, list):
        self.session.add_all(list)
        self.session.commit()

    
