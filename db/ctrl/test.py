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

