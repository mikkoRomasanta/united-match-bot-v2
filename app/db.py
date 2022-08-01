from xmlrpc.client import Boolean
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, Text, Date, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import update
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv('SQLALCHEMY_DB_URI'))
base = declarative_base()

class Application(base):
    __tablename__ = 'application'
    
    id = Column(Integer, primary_key=True)
    data = Column(Text)
    type = Column(String(255))
    date = Column(Date, default=datetime.now())
    
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        
base.metadata.create_all(engine)

def load_session():
    Session = sessionmaker(bind=engine)
    session = Session()

    return session

def close_session(session):
    session.close()
    engine.dispose()
    
    return