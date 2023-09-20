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
    
class NotUsedMarker(Base):
    __tablename__ = "not_used_marker"
    id = Column(Integer,primary_key=True)
    mark = Column(Integer)
    
class UsingMarker(Base):
    __tablename__ = "using_marker"
    id = Column(Integer,primary_key=True)
    mark = Column(Integer)
    user_name = Column(String(255))
    
class DataBaseTools(): ###もっと分業させる
    def __init__(self,Bases):
        engine = create_engine("sqlite:///db/database",echo=True)
        Bases.metadata.create_all(engine)    

        SessionClass = sessionmaker(engine)
        self.session =  SessionClass()

    
    def insert(self,data):
        self.session.add(data)
        self.session.commit()
    
    def delete(self,data):
        self.session.delete(data)
        self.session.commit()
        
    def update(self):
        self.session.commit()
        
        
    def get_all(self,table):
        datas = self.session.query(table).order_by(desc(table.id)).all()
        return datas
    
    def get_limit(self,table,limit):
        datas =  self.session.query(table).limit(limit).all()
        return datas
    
    def get_last(self,table):
        data = self.session.query(table).order_by(table.id.desc()).first()
        return data
    
    def search_name(self,table,data):
        datas = self.session.query(table).filter(table.user_name==data).all()
        return datas
    
    def search_user(self,table,mode):
        if mode:
            datas = self.session.query(table).filter(table.user_name=="").all()
        else:
            datas = self.session.query(table).filter(table.user_name!="").all()
        return datas
    
    def search_aruco(self,table,mark):
        datas = self.session.query(table).filter(table.mark==mark).first()
        return datas
    
    def make_some_marker(self,start,num):
        for i in range(start ,start + num):
            data = NotUsedMarker(mark=i)
            print("add" + str(i))
            self.insert(data)