import sys
sys.path.append('../')
import db.table_cr as db
#import table_cr as db
from common import Ctrl

class News(Ctrl):
    def __init__(self, session):
        '''
        joint session
        '''
        Ctrl.__init__(session, db.News)

    def add(self, news):
        self.commit(news)
