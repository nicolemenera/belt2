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
  context = {'loggeduser':User.objects.get(id=request.session['userid']), 'quotes':Quote.objects.all(), 'favorites': Quote.objects.exclude(likers__id=request.session['userid'])}
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
  
def add(request):
  if 'userid' not in request.session:
    return redirect('/')
  print "adding quote to favorites!"
  quote_id = request.POST['qid']
  this_quote = Quote.objects.get(id=quote_id)
  this_user = User.objects.get(id=request.session['userid'])
  this_quote.likers.add(this_user)
  print request.POST
  return redirect('/dashboard')
  
def remove(request):
  print "removing quote from favorites..."
  return redirect('/dashboard')
  
def user(request):
  print "we here!"
  return render(request, 'quotes/user.html')
  
def logout(request):
  print "logging out!"
  if request.method == "GET":
    return redirect('/')
  del request.session['userid']
  return redirect('/')
