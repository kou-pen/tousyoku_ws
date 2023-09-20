from sqlalchemy import *
from sqlalchemy.orm import *


Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    user_name  = Column(String(255))
    file_name  = Column(String(255))
    
class Data(Base):
    __tablename__ = "data"
    id  = Column(Integer, primary_key=True)
    mark = Column(String(255))
    user_name = Column(String(255))
    
class DataBaseTools():
    def __init__(self,Base):
        engine = create_engine("sqlite:///database",echo=True)
        Base.metadata.create_all(engine)    

        SessionClass = sessionmaker(engine)
        self.session =  SessionClass()
    
    def insert(self,data):
        self.session.add(data)
        self.session.commit()
    
    def delete(self,data):
        self.session.delete(data)
        self.session.commit()
        
        
        
db_tools  =  DataBaseTools(Base)
user_a = User(user_name = "kohki",file_name = "file")
db_tools.insert(user_a)
user_b = Data(mark = "1234",user_name = "kohki")
db_tools.insert(user_b)