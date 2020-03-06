#!/usr/bin/python3
"""Request handlers for the uWeb3 project scaffold"""

import uweb3
from uweb3 import alchemy_model
from uweb3 import PageMaker, SqAlchemyPageMaker
from uweb3.pagemaker.new_login import Users, UserCookie, Test
from uweb3.pagemaker.new_decorators import checkxsrf

from sqlalchemy import Column, Integer, String, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
class User(alchemy_model.Record, Base):
  __tablename__ = 'users'

  id = Column(Integer, primary_key=True)
  username = Column(String, nullable=False, unique=True)
  password = Column(String, nullable=False)    
      
class Author(alchemy_model.Record, Base):
  __tablename__ = 'author'

  id = Column(Integer, primary_key=True)
  name = Column(String, unique=True)
  
class Persons(alchemy_model.Record, Base):
  __tablename__ = 'persons'
  
  id = Column(Integer)
  name = Column(String, primary_key=True)
         
class UserPageMaker(SqAlchemyPageMaker):
  """Holds all the request handlers for the application"""
  
  def Login(self):
    """Returns the index template"""
    # aut = Author(self.session, {'name': 'stef'})
    # result = User.Create(self.session, {'username': 'name', 'password': 'test'})
    # print("Created: ", result)
    user = User.FromPrimary(self.session, 12)
    print(user.TableName())
    # # print("FromPrimary: ", user)
    # print(user)
    # user.id = 1
    # user.Save()
    # print(user)
    # print("List: ", list(User.List(self.session, order=(User.id.desc(), User.username.asc()))))
    # print("DeletePrimary: ", User.DeletePrimary(self.session, result.id))
    # print("List: ", User.List(self.session, conditions=[{'id': '10', 'operator': '<='}]))
    
    # person = Persons.Create(self.session, {'id': 1, 'name': 'test2'})

    # self.session.add(aut)
    # self.session.add(user)
    # user = self.session.query(User).filter_by(id=1).first()
    # user.username = "test"
    # print(self.session.new)
    # print(self.session.dirty)
    # self.session.commit()
    # print(self.session.query(User).filter_by(username='noname').first())
    
    return 200
    # self.session.close()
    # print(self.session.query(User).filter_by(username='test'))
    
    # print(self.session.query(Author).filter_by(name=2).first())    
    # session.add(user)
    scookie = UserCookie(self.secure_cookie_connection)
    # test = Test()
    if self.req.method == 'POST':
      try:
        user = Users()
        # user = user.FromPrimary(self.connection, self.session, 1)
        if Users.ComparePassword(self.post.get('password'), user['password']):
          scookie.Create("login", {
                'user_id': user['id'],
                'premissions': 1,
                'data': {'data': 'data'}
                })
          return self.req.Redirect('/test')
        else:
          print('Wrong username/password combination')      
      except uweb3.model.NotExistError as e:
        print(e)
        
    return self.parser.Parse('login.html')

  @checkxsrf
  def Logout(self):
    scookie = UserCookie(self.secure_cookie_connection)
    scookie.Delete('login')
    return self.req.Redirect('/login')