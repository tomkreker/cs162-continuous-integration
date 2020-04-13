import requests

# post  valid expression
r = requests.post('http://192.168.99.100:5000/add', data = {'expression': '1+2+3'})

# check the correct response was received
if r.status_code != 200:
	raise Exception('failed to post')
	
# check you would see the answer
if '6.00 = 1+2+3' not in r.text:
	raise Exception('did not get and present a correct answer')
	
import psycopg2 #for postgres
from sqlalchemy import create_engine, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


#connection string from stack overflow + details form Docker Compose file
con_string = 'postgres+psycopg2://cs162_user:cs162_password@192.168.99.100:5432/cs162'
engine = create_engine(con_string)
engine.connect() 

Base = declarative_base() 

class Expr(Base):
    __table__ = Table('expression', Base.metadata,
                    autoload=True, autoload_with=engine)

Session = sessionmaker(bind=engine)
s = Session()

#print (Expr.__table__.c) #display column names

#get latest item inserted
latest = s.query(Expr).order_by(Expr.now.desc()).first()
if latest.text != '1+2+3' or latest.value != 6:
	raise Exception('Latest query not saved in the db')

# post faulty query
r2 = requests.post('http://192.168.99.100:5000/add', data = {'expression': '1///2+3'})

if r2.status_code != 500: #should be an erorr
	raise Exception('posted a faulty query')

latest = s.query(Expr).order_by(Expr.now.desc()).first()
if latest.text != '1+2+3' or latest.value != 6:
	raise Exception('A new item was inserted - boo')
	

print ('All tests have passed')