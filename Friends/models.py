from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from stories.models import *
from cloudinary.models import CloudinaryField
# Create your models here.
class Friend_request(models.Model):
    sender = models.IntegerField()
    receiver = models.IntegerField()
    is_accepted = models.BooleanField(default=False)
    
def request_sender(id):
    request_sender = Friend_request.objects.filter(Q(sender = id)|Q(receiver = id))
    if request_sender:
        return request_sender

class Friend(models.Model):
    sender = models.IntegerField()
    receiver = models.IntegerField()
    is_blocked = models.BooleanField(default=False)

def get_all_friends_user(id):
    friends = Friend.objects.filter(Q(sender = id) | Q(receiver = id))
    friend_list=[]
    for i in friends:
        if i.sender is not id:
            friend_list+=User.objects.filter(id=i.sender)
        else:
            friend_list+=User.objects.filter(id=i.receiver)
    return friend_list

def get_all_friends(id):
    friends = Friend.objects.filter(Q(sender = id) | Q(receiver = id))
    return friends

def get_mutual_friends(id,sid):
    mero_friends=list(get_all_friends_user(id))
    usko_sathi=list(get_all_friends_user(sid))
    a=len([element for element  in mero_friends if element in usko_sathi])
    return a

class Profile(models.Model):
    profile_picture = models.ImageField(upload_to = 'user-profile/',default='avatar.svg')
    user = models.OneToOneField(User,on_delete = models.CASCADE,null=True)
    age = models.IntegerField(null=True)
    job = models.CharField(max_length = 100,null=True)
    bio = models.TextField(null=True)
    address = models.CharField(max_length = 100,null=True)
    contact_no = models.IntegerField(null=True)
def get_friend_request_list(userid):
    request_list=[]
    friend_request=Friend_request.objects.filter(receiver=userid)
    for i in friend_request:
        request_list+=User.objects.filter(id=i.sender)
    for i in request_list:
        i.is_received=True
        i.mutual_friends=get_mutual_friends(userid,i.id)

    return request_list
def get_sent_request_list(userid):
    request_list=[]
    friend_request=Friend_request.objects.filter(sender=userid)
    for i in friend_request:
        request_list+=User.objects.filter(id=i.receiver)
    for i in request_list:
        i.is_sent=True
        i.mutual_friends=get_mutual_friends(userid,i.id)

    return request_list
def get_friend_suggestion(userid,user):
    friend_suggestion=[]
    suggestion=[]
    count=[]
    my_friend=get_all_friends_user(userid)
    for i in my_friend:
        i.friends=get_all_friends_user(i.id)
        suggestion+=set(i.friends)-set(my_friend)
        for j in suggestion:
            if j.id is not i.id:
                try:
                    sent=Friend_request.objects.get(Q(sender=userid)|Q(receiver=userid))
                    friend_suggestion+=User.objects.filter(id=j.id).exclude(id=sent.receiver).exclude(id=sent.sender)
                except:
                    friend_suggestion+=User.objects.filter(id=j.id)
    friend_suggestion=list(dict.fromkeys(friend_suggestion))
    if friend_suggestion:
        try:
            friend_suggestion.remove(user)
        except:
            pass
        for k in friend_suggestion:
            k.mutual_friends=get_mutual_friends(userid,k.id)


    else:
        friend_suggestion+=User.objects.filter(username="dev")
        friend_suggestion+=User.objects.filter(username="santosh")
    for i in friend_suggestion:
        i=attach_status(userid,i)
    return friend_suggestion

def get_friendship_status(myid,userid):
    status="notfriend"
    sent_req=Friend_request.objects.filter(sender=myid).filter(receiver=userid)
    if sent_req:
       status='sent' 
    else:
        received_req=Friend_request.objects.filter(sender=userid).filter(receiver=myid)
        if received_req :
            status='received'
        else:
            friend1=Friend.objects.filter(sender=myid).filter(receiver=userid)
            friend2=Friend.objects.filter(sender=userid).filter(receiver=myid)
            if friend1:
                status='friend'
            
            elif friend2:
                status='friend'
    return status
def attach_status(myid,user):
    status=get_friendship_status(myid,user.id)

    if(status=="sent"):
        user.is_sent=True
       
    elif(status=="received"):
        user.is_received=True
        
    elif(status=="friend"):
        user.is_friend=True
        
    elif(status=="notfriend"):
        user.is_not_friend=True
        
    return user
    
def add_user_to_post(post,user):
        friend_list=get_all_friends_user(user.id)
        posttosee=PostForUser()
        posttosee.user=user
        posttosee.post=post
        posttosee.save()
        for i in friend_list:
            posttosee=PostForUser()
            posttosee.user=i
            posttosee.post=post
            posttosee.save()
        return True
    
def assign_users_to_my_post(cuser,user):
        mystories=Post.objects.filter(user=cuser).order_by("-id")[:3]
        hisstories=Post.objects.filter(user=user).order_by("-id")[:3]
        for story in mystories:
            posttosee=PostForUser()
            posttosee.user=user
            posttosee.post=story
            posttosee.save()
        for story in hisstories:
            posttosee=PostForUser()
            posttosee.user=cuser
            posttosee.post=story
            posttosee.save()
        return True

def remove_users_from_my_post(request,user):
    mystories=get_stories_user(request,request.user)[0]
    hisstories=get_stories_user(request,user)[0]
    for story in mystories:
        postuser=PostForUser.objects.filter(post=story).filter(user=user)
        for p in postuser:
            p.delete()
    for story in hisstories:
        postuser=PostForUser.objects.filter(post=story).filter(user=request.user)
        for p in postuser:
            p.delete()
    return True  

    

