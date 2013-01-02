import sys
sys.path.append('../')
import db.table_cr as db
#import table_cr as db
from common import Ctrl

class TagKind(Ctrl):
    def __init__(self, session):
        '''
        joint session
        '''
        Ctrl.__init__(session, db.TagKind)

    def addTag_byId(self, id, tag):
        #ck = self.session.query(db.TagKind).filter(db.TagKind.id == id).first()
        self.setCur(id)
        self.cur.tags.append(tag)
        self.commit_all([self.cur, tag])

class Tag(Ctrl):
    def __init__(self, session):
        '''
        joint session
        '''
        Ctrl.__init__(session, db.Tag)
    
