from django.shortcuts import render, redirect, HttpResponse
from .models import User, Quote
from django.contrib import messages
from datetime import datetime
# Create your views here.

def index(request):
  print "we here!"
  return render(request, 'quotes/index.html')
  
def register(request):
  if request.method=='GET':
    return redirect('/')
    print "registering"
  user = User.objects.register(request.POST)
  if 'reg_error' in user:
    error = user['reg_error']
    for msg in error:
      messages.error(request, msg)
    return redirect('/')
  else:
    user = User.objects.filter(email = request.POST['email'])
    request.session['userid'] = user[0].id
    print "VIEWS REGISTERED!"
  return redirect('/dashboard')
  
def login(request):
  print "logging in!"
  if request.method=='GET':
    return redirect('/')
  user = User.objects.login(request.POST)
  if 'login_error' in user:
    error = user['login_error']
    for msg in error:
      messages.error(request, msg)
    return redirect('/')
  else:
    user = User.objects.filter(email = request.POST['email'])
    request.session['userid'] = user[0].id
  return redirect('/dashboard')
  
def dashboard(request):
  if 'userid' not in request.session:
    return redirect('/')
  nonefavorites = []
  favorites = []
  quotes = Quote.objects.all()
  loggeduser = User.objects.get(id=request.session['userid'])
  
  for q in quotes:
    foundUser = False
    for likes in q.likers.all():
      if likes == loggeduser:
        foundUser = True
        favorites.append(q)
    if foundUser == False:
      nonefavorites.append(q)
      print likes.name
  context = {'loggeduser': loggeduser, 'nonefavorites': nonefavorites, 'favorites': favorites}
  return render(request, 'quotes/dashboard.html', context)
  
def submit(request):
  if 'userid' not in request.session:
    return redirect('/')
  quote = Quote.objects.submit(request.POST, User.objects.get(id=request.session['userid']))
  if 'submit_error' in quote:
    error = quote['submit_error']
    for msg in error:
      messages.error(request, msg)
    return redirect('/dashboard')
  else:
    messages.success(request, "Quote Added!")
  print "posting quote!"
  return redirect('/dashboard')
  
def add(request, quoteid):
  if 'userid' not in request.session:
    return redirect('/')
  print "adding quote to favorites!"
  addQuote = Quote.objects.add(request.session['userid'], quoteid)
  print request.POST
  return redirect('/dashboard')
  
def remove(request, quoteid):
  if 'userid' not in request.session:
    return redirect('/')
  print "removing quote from favorites..."
  removeQuote = Quote.objects.remove(request.session['userid'], quoteid)
  print request.POST
  return redirect('/dashboard')
  
def user(request, userid):
  if 'userid' not in request.session:
    return redirect('/')
  userQuotes = []
  noQuotes = []
  count = 0
  quotes = Quote.objects.all()
  userInfo = User.objects.get(id=userid)
  
  for q in quotes:
    foundUser = False
    if q.creator == userInfo:
      foundUser = True
      userQuotes.append(q)
      count = count + 1
    if foundUser == False:
      noQuotes.append("User hasn't created any posts")
  print userQuotes
  context = {'userInfo': userInfo, 'noQuotes': noQuotes, 'userQuotes': userQuotes, 'count': count}
  return render(request, 'quotes/user.html', context)
  
def info(request, userid):
  
  print "made it to info!"
  return redirect('/user/'+ userid)
  
def logout(request):
  print "logging out!"
  if request.method == "GET":
    return redirect('/')
  del request.session['userid']
  return redirect('/')
