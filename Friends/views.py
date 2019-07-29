from django.shortcuts import render,redirect,HttpResponse
from .models import *
from django.contrib.auth.models import User
from stories.models import *
from Friends.models import *
import random
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required(login_url='/login/')
def profile(request):
    if request.method=='POST':
        new_story=Post()
        new_story.body = request.POST['add_story']
        new_story.user = request.user
        new_story.save()
        return redirect('/profile/my_profile/')    
    request_list=[]
    friend_request=Friend_request.objects.filter(receiver=request.user.id)
    for i in friend_request:
        request_list+=User.objects.filter(id=i.sender)

    
    friend_list=[]
    friends = get_all_friends(request.user.id)
    for i in friends:
        if i.sender is not request.user.id:
            friend_list+=User.objects.filter(id=i.sender)
        else:
            friend_list+=User.objects.filter(id=i.receiver)
    stories=Post.objects.filter(user=request.user).order_by('-id')
    for story in stories:
        story.like=Like.objects.filter(post=story)
    profile = User.objects.get(id=request.user.id)
    friend_suggestion=[]
    suggestion=[]
    count=[]
    my_friend=get_all_friends_user(request.user.id)
    
        
    for i in my_friend:
        i.friends=get_all_friends_user(i.id)
        suggestion+=set(i.friends)-set(my_friend)
        for j in suggestion:
            if j.id is not i.id:
                try:
                    sent=Friend_request.objects.get(Q(sender=request.user.id)|Q(receiver=request.user.id))
                    friend_suggestion+=User.objects.filter(id=j.id).exclude(id=sent.receiver)
                except:
                    friend_suggestion+=User.objects.filter(id=j.id)
    friend_suggestion=list(dict.fromkeys(friend_suggestion))
    if friend_suggestion:
        friend_suggestion.remove(request.user)
        for k in friend_suggestion:
            k.mutual=get_mutual_friends(request.user.id,k.id)
        random.shuffle(friend_suggestion)

    else:
        friend_suggestion+=User.objects.filter(id=1)
    request.notification=get_last_ten(request.user)
    return render(request,'profile.html',{'friend_suggestion':friend_suggestion,'profile':profile,'page-title':request.user,'stories':stories,'friend_list':friend_list,'request_sender':request_list})
@login_required(login_url='/login/')
def delete(request,id):
    if request.method=='POST':
        delete= Post.objects.get(id =id)
        delete.delete()
        return redirect('/profile/')
@login_required(login_url='/login/')
def accept_request(request,id):
    if request.method =='POST':
        new_friend=Friend()
        new_friend.sender= id
        new_friend.receiver =request.user.id
        new_friend.save()
        user=User.objects.get(id = id)
        set_notification(user,request.user.first_name +' '+ request.user.last_name + ' accepted your Connect Request.',0,'/profile/'+request.user.username+'/')
        friend_request = Friend_request.objects.filter(sender = id)
        for i in friend_request:
            i.delete()
        return redirect('/profile/my_profile/')
@login_required(login_url='/login/')
def deny_request(request,id):
    friend_request = Friend_request.objects.filter(sender = id)
    for i in friend_request:
        i.delete()
    return redirect('/profile/my_profile/')
@login_required(login_url='/login/')
def send_request(request,id):
    if request.method=='POST':
        request_obj=Friend_request.objects.filter(sender=id).filter(receiver=request.user.id)
        request_obj2=Friend_request.objects.filter(sender=request.user.id).filter(receiver=id)
        if not request_obj:
            if not request_obj2:
                add_request = Friend_request()
                add_request.sender = request.user.id
                add_request.receiver = id
                add_request.save()
                user=User.objects.get(id = id)
                set_notification(user,request.user.first_name+' '+request.user.last_name +' sent you Connect Request.',0,'/profile/'+request.user.username+'/')
                return redirect('/profile/my_profile/')
            else:
                return redirect('/profile/my_profile/')
        else:
            return redirect('/profile/my_profile/')
    else:
        return redirect('/profile/my_profile/')
@login_required(login_url='/login/')
def user_profile(request,username):
    try:
        user = User.objects.get(username = username)
        stories = Post.objects.filter(user = user)
        for story in stories:
            story.like=Like.objects.filter(post=story)
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
        request.notification=get_last_ten(request.user)
        return render(request,'friend_profile.html',{'user':user,'stories':stories,'friend_suggestion':friend_suggestion,'friend_list':friend_list,'request_sender':request_list})
    except:
        user = 0
        return redirect('/profile/my_profile/')
@login_required(login_url='/login/')
def unfriend(request,id):
    try:
        friend=Friend.objects.filter(Q(sender=request.user.id) |Q(sender=id)).filter(Q(receiver=request.user.id) |Q(receiver=id)).get()
        if friend:
            friend.delete()
        else:
            return redirect('/profile/my_profile/')  
    except:
        return redirect('/profile/my_profile/')     
    return redirect('/profile/my_profile/') 
@login_required(login_url='/login/')
def update_profile(request):
    if request.method=='POST':
        
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        age=request.POST['age']
        address=request.POST['address']
        job=request.POST['job']
        contact_no=request.POST['contact_no']
        bio=request.POST['bio']
        
        try:
            profile=Profile.objects.get(user=request.user)
        except:
            profile=Profile()
            profile.user=request.user
        user=User.objects.get(id=request.user.id)
        if first_name:
            user.first_name=first_name
        if last_name:
            user.last_name=last_name
        if age:
            profile.age=age
        if address:
            profile.address=address
        if contact_no:
            profile.contack_no=contact_no
        if bio:
            profile.bio=bio
        if job:
            profile.job=job
        profile.save()
        user.save()
        return redirect('/profile/my_profile/')
