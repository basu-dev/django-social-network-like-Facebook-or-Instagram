from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
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
    profile_picture = models.ImageField(upload_to = 'user-profile/',default='default_pp.png')
    user = models.OneToOneField(User,on_delete = models.CASCADE,null=True)
    age = models.IntegerField(null=True)
    job = models.CharField(max_length = 100,null=True)
    bio = models.TextField(null=True)
    address = models.CharField(max_length = 100,null=True)
    contack_no = models.IntegerField(null=True)

