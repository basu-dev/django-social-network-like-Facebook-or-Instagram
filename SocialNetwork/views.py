from django.shortcuts import render,redirect,HttpResponse
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
            fe.username_error='User already exits!'
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
            return render(request,'account/signup_view.html',{'page_title':'signup-ElectronisHub','formerror':fe,'username':ue,'password':pe,'first_name':ne,'data':newuser})

    else:
        return render(request,'account/signup_view.html',{'page_title':'signup-ElectronisHub','formerror':fe})

def login_view(request):
    fe=formerror()
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user:
            login(request,user)
            return redirect('/')
        else:
            fe.message='Username/password error please provede correct credentials'
            return render(request,'account/login_view.html',{'page_title':'Login-ElectronicsHub','formerror':fe})  
    else:
        return render(request,'account/login_view.html',{'page_title':'Login-ElectronicsHub','formerror':fe}) 
@login_required(login_url='/login/')
def search(request):         
    friend_list = get_all_friends_user(request.user.id)
    request_list=[]
    friend_request=Friend_request.objects.filter(receiver=request.user.id)
    for i in friend_request:
        request_list+=User.objects.filter(id=i.sender)
    friend_suggestion=[]
    suggestion=[]
    count=[]
    my_friend=get_all_friends_user(request.user.id)
    for i in my_friend:
        i.friends=get_all_friends_user(i.id)
        suggestion+=set(i.friends)-set(my_friend)
        for j in suggestion:
            if j.id is not i.id:
                friend_suggestion+=User.objects.filter(id=j.id)
    friend_suggestion=list(dict.fromkeys(friend_suggestion))
    if friend_suggestion:
        friend_suggestion.remove(request.user)
        for k in friend_suggestion:
            k.mutual=get_mutual_friends(request.user.id,k.id)
        random.shuffle(friend_suggestion)

    else:
        friend_suggestion+=User.objects.filter(id=1)
    try:
        searchdata=request.GET['search_query']
        if searchdata:
            users=User.objects.filter(Q(username__contains=searchdata) |Q(first_name__contains=searchdata) | Q(last_name__contains=searchdata)).exclude(id=request.user.id)
            for i in users:
                i.friend=Friend.objects.filter(Q(sender=request.user.id) |Q(sender=i.id)).filter(Q(receiver=request.user.id) |Q(receiver=i.id))
                if i.friend:
                    i.is_my_friend=True
                else:
                    i.is_my_friend=False
    except:
        user=0
    request.notification=get_last_ten(request.user)
    return render(request,'search.html',{'users':users,'friend_suggestion':friend_suggestion,'friend_list':friend_list,'request_sender':request_list})
    