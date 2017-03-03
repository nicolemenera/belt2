from __future__ import unicode_literals

from django.db import models
import re
import bcrypt
import datetime
NAME_REGEX = re.compile(r'[a-zA-Z]\D{2,}$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.

class UserManager(models.Manager):
  def register(self, data):
    status = True
    errorList = []
    today = str(datetime.datetime.today()).split()[0]
    
    if len(data['name']) < 1:
      status = False
      errorList.append("Name must be given")
    if len(data['name']) < 2:
      status = False
      errorList.append("Name must be greater than two letters in length")
    if not NAME_REGEX.match(data['name']):
      status = False
      errorList.append("Name may only contain letters")
    if len(data['alias']) < 2:
      status = False
      errorList.append("Alias must be greater than two characters in length")
    if len(data['email']) < 2:
      status = False
      errorList.append("An email must be provided")
    if not EMAIL_REGEX.match(data['email']):
      status = False
      errorList.append("Invalid email")
    if len(data['password']) < 1:
      status = False
      errorList.append("A password must be provided")
    if len(data['password']) < 8:
      status = False
      errorList.append("Password must be greater than eight characters in length")
    if data['password'] != data['confirm_pw']:
      status = True
      errorList.append("Passwords must match!")
    if data['dob'] > today:
      status = False
      errorList.append("Date of birth cannot be a future date")
    if len(data['dob']) < 8:
      status = False
      errorList.append("Invalid Date of Birth")
    if len(data['dob']) == 0:
      status = False
      errorList.append("Date of Birth must be provided")
    if status == False:
      print today
      return {'reg_error':errorList}
    if status == True:
      password = data['password']
      hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
      User.objects.create(name=data['name'], alias=data['alias'], email=data['email'], password=hashed, dob=data['dob'])
      print "MODEL REGISTERED!"
    return {}
    
  def login(self, data):
    status = True
    errorList = []
    
    user = User.objects.filter(email=data['email'])
    if len(data['email']) < 2:
      status = False
      errorList.append("Email must be provided to log in!")
    if len(user) < 1:
      status = False
      errorList.append("Email does not exist, please register!")
    if status == False:
      return {'login_error' : errorList}
    else: 
      if bcrypt.hashpw(data['password'].encode(), user[0].password.encode()) == user[0].password:
        return {}
      else:
        errorList.append("Password does not match record")
        return {'login_error' : errorList}

class User(models.Model):
  name = models.CharField(max_length=255)
  alias = models.CharField(max_length=255)
  email = models.CharField(max_length=255)
  password = models.CharField(max_length=255)
  dob = models.DateField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = UserManager()
  
  
class QuoteManager(models.Manager):
  def submit(self, data, user):
    status = True
    errorList = []
    
    if len(data['quoteby']) < 4:
      status = False
      errorList.append("Quoted By must be more than three characters in length")
    if len(data['quoteinput']) < 10:
      status = False
      errorList.append("Message length must be 10 or more characters long")
    if status == False:
      return {'submit_error' : errorList}
    else:
      new_quote = Quote.objects.create(creator=user, quote_author=data['quoteby'], quote=data['quoteinput'])
      return{}
      
  def add(self, userid, quoteid):
    this_quote = Quote.objects.get(id=quoteid)
    this_user = User.objects.get(id=userid)
    this_quote.likers.add(this_user)
    return {}
    
  def remove(self, userid, quoteid):
    this_quote = Quote.objects.get(id=quoteid)
    this_user = User.objects.get(id=userid)
    this_quote.likers.remove(this_user)
    return {}
  
class Quote(models.Model):
  creator = models.ForeignKey(User, related_name = "createdquotes")
  quote_author = models.CharField(max_length=255)
  quote = models.CharField(max_length=255)
  likers = models.ManyToManyField(User, related_name = "userlikers")
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = QuoteManager()