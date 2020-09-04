from django.shortcuts import render,redirect,HttpResponse
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from stories.models import *
from stories.models import *
from Friends.models import *
from django.core.files.storage import FileSystemStorage
import random
@login_required(login_url='/login/')
def log_out(request):
    if request.method=='POST':
        if request.user.is_authenticated:
            logout(request)
            return redirect('/login/')
        else:
            return redirect('/login/') 
    else:
        return redirect('/login/')      
class formerror():
    def __init__(self):
        self.username_error=''
        self.password_error=''
        self.name_error=''

def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    fe=formerror()
    ne=''
    pe=''
    ue=''
    newuser=User()
    if request.method=='POST':
        newuser.username=request.POST['username']
        newuser.password1=request.POST['password1']
        newuser.password2=request.POST['password2']
        newuser.first_name=request.POST['first_name']
        newuser.last_name=request.POST['last_name']
        if(request.POST['username']=="my_profile"):
            fe.username_error="Invalid username. Choose New One."
            return render(request,'account/signup_view.html',{'page_title':'Raven-Signup','formerror':fe,'newuser':newuser})
        validation=1
        if newuser.password1==newuser.password2:
            if len(newuser.password1)<6:
                fe.password_error='Password must be grater than 6 digits!'
                pe='is-invalid'
                validation=0
        else:
            fe.password_error='Two password didnot match!'
            pe='is-invalid'
            validation=0
        try:
            user=User.objects.filter(username=newuser.username).get()
        except:
            user=0
            ue='is-valid' 
        if user:
            fe.username_error='Username already exits!'
            validation=0
            ue='is-invalid'
        if newuser.first_name and newuser.last_name:
            v=1
        else :
            validation=0
            fe.name_error='First and last name is required!'
            ne='is-invalid'
        if validation:
            newuser.set_password(newuser.password1)
            newuser.save()
            pp=Profile()
            pp.user=newuser
            pp.save()
            return redirect('/login/')
        else:
            return render(request,'account/signup_view.html',{'page_title':'Raven-Signup','formerror':fe,'username':ue,'password':pe,'first_name':ne,'newuser':newuser})
    else:
        return render(request,'account/signup_view.html',{'page_title':'Raven-Signup','formerror':fe})

def username_validate(request):
    if request.method=='POST':
        value=request.POST['value']
        if(value=="my_profile"):
            return JsonResponse({"invalid":True,"exist":False})
        try:
            user=User.objects.get(username=value)
            return JsonResponse({"exist":True,"invalid":False})
        except:
            return JsonResponse({"exist":False,"invalid":False})
def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    fe=formerror()
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user:
            login(request,user)
            return redirect('/')
        else:
            fe.message='Username/password error please provide correct credentials'
            return render(request,'account/login_view.html',{'page_title':'Login-ElectronicsHub','formerror':fe})  
    else:
        return render(request,'account/login_view.html',{'page_title':'Raven-Login','formerror':fe}) 
@login_required(login_url='/login/')
def search(request):         
    try:
        searchdata=request.GET['search_query']
        if searchdata:
            users=User.objects.filter(Q(username__contains=searchdata) |Q(first_name__contains=searchdata) | Q(last_name__contains=searchdata)).exclude(id=request.user.id)
            for i in users:
                i.mutual_friends=get_mutual_friends(request.user.id,i.id)
                i=attach_status(request.user.id,i)
    except:
        users=0
    request.search=True
    return render(request,'search.html',{'users':users})
