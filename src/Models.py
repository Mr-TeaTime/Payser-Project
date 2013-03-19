import datetime
from google.appengine.ext import db
from google.appengine.api import users


class Employee(db.Model):
    userid = db.StringProperty()
    name = db.StringProperty()
    email = db.StringProperty()
    
    income = db.IntegerProperty()
    tax = db.IntegerProperty()
    net = db.IntegerProperty()
    company = db.StringProperty()
    
class Employer(db.Model):
    userid = db.StringProperty()
    name = db.StringProperty()
    email = db.StringProperty()
    join_date = db.DateProperty()
    company = db.StringProperty()
    
    
    
class Payslip(db.Model):
    ownerId = db.StringProperty()
    upload_date = db.DateProperty(auto_now_add=True)
    beginning =  db.DateProperty()
    ending =  db.DateProperty()
    income = db.FloatProperty()
    tax = db.FloatProperty()
    net = db.FloatProperty()
    company = db.StringProperty()
    
class File(db.Model):
    ownerId = db.StringProperty()
    title = db.StringProperty()
    description = db.StringProperty()
    upload_date = db.DateProperty(auto_now_add=True)
    data = db.BlobProperty()
    mimetype = db.StringProperty()
    
def payslip_key(owner_id):
  return db.Key.from_path('Payslip', owner_id)

def file_key(owner_id):
  return db.Key.from_path('File', owner_id)
    
    

