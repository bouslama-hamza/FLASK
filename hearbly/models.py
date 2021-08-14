from enum import unique
from hearbly import db
from hearbly import app
#create a class for the user
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(50),unique = True, nullable= False)
    password = db.Column(db.String(50), nullable= False)
    def __repr__(self):
        return f"User('{self.id}','{self.email}','{self.password}')"
#create user class
class Register(db.Model):
    id = id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20) , nullable = False)
    l_name = db.Column(db.String(20) , nullable = False)
    email = db.Column(db.String(50),unique = True, nullable= False)
    password = db.Column(db.String(50), nullable= False)
    confirm_password = db.Column(db.String(50), nullable= False)
    phone = db.Column(db.String(20) , nullable = False)
    def __repr__(self):
        return f"Register('{self.id}','{self.name}','{self.l_name}','{self.email}','{self.password}','{self.confirm_password}','{self.phone}')"