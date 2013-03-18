import datetime
from google.appengine.ext import db
from google.appengine.api import users


class Employee(db.Model):
    userid = db.StringProperty()
    name = db.StringProperty(required=True)
    email = db.StringProperty(required=True)
    join_date = db.DateProperty(required=True)
    income = db.IntegerProperty()
    tax = db.IntegerProperty()
    net = db.IntegerProperty()
    employer = db.StringProperty()
    
class Employer(db.Model):
    userid = db.StringProperty()
    name = db.StringProperty(required=True)
    email = db.StringProperty(required=True)
    join_date = db.DateProperty(required=True)
    company = db.StringProperty(required=True)
    
class Payslip(db.Model):
    owner = db.StringProperty(required=True)
    title = db.StringProperty(required=True)
    upload_date = db.DateProperty(required=True)
    beginning =  db.DateProperty()
    ending =  db.DateProperty()
    income = db.IntegerProperty()
    tax = db.IntegerProperty()
    net = db.IntegerProperty()
    company = db.StringProperty(required=True)
    
class File(db.Model):
    owner = db.StringProperty(required=True)
    title = db.StringProperty(required=True)
    upload_date = db.DateProperty(required=True)
    data = db.BlobProperty(required=True)
    mimetype = db.StringProperty(required=True)
    
    

