from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
class Test(models.Model):
    prop=models.TextField()
# Create your models here.
class Message(models.Model):
    sender = models.IntegerField()
    receiver = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
    seen =models.BooleanField(default=False)
    del_by_sender = models.IntegerField(default=0)
    del_by_receiver =models.IntegerField(default=0)
    delivered = models.BooleanField(default = False)
    def get_name(self):
        return User.objects.get(id=self.sender).first_name
    #for receiver's name in messanger
    def get_receiver_name(self):
        return User.objects.get(id=self.receiver).first_name

def get_message_with(u_id,id):
    messages = Message.objects.filter(Q(sender=u_id)|Q(receiver=u_id)).filter(Q(sender=id)|Q(receiver=id)).exclude(Q(del_by_sender = u_id)|Q(del_by_receiver=u_id)).order_by("-id")[:15]
    updated_messages=[]
    i=len(messages)-1
    while(i>=0):
        updated_messages+=Message.objects.filter(id=messages[i].id)
        i=i-1
    try:
        lastid=updated_messages[0].id
    except:
        lastid=0
    return (updated_messages,lastid)
def get_more_message_with(u_id,id,lastid):
    messages = Message.objects.filter(Q(sender=u_id)|Q(receiver=u_id)).filter(Q(sender=id)|Q(receiver=id)).exclude(Q(del_by_sender = u_id)|Q(del_by_receiver=u_id)).filter(id__lt=lastid).order_by("-id")[:10]
    updated_messages=[]
    i=len(messages)-1
    while(i>=0):
        updated_messages+=Message.objects.filter(id=messages[i].id)
        i=i-1
    try:
        lastid=updated_messages[0].id
    except:
        lastid=0
    return (updated_messages,lastid)
def get_last_message_with(u_id,id):
    messages = Message.objects.filter(Q(sender=u_id)|Q(receiver=u_id)).filter(Q(sender=id)|Q(receiver=id)).exclude(Q(del_by_sender = u_id)|Q(del_by_receiver=u_id)).last()
    last_message=[]
    if messages:
        last_message_id=messages.id
        last_message=Message.objects.filter(id=last_message_id)
    return last_message

class Message_Notification(models.Model):
    sender=models.IntegerField()
    receiver=models.IntegerField()
    seen=models.BooleanField(default=False)
def get_last_message_body_homepage(userid,friend_list):
    message_body=[]
    for i in friend_list:
       message_body+= get_last_message_with(userid,i.id)
           #was error while applying if inside storylin so we used if inside views (gettin the name of our friend but not ours)
    for i in message_body:
        if i.sender==userid:
            name=User.objects.get(id=i.receiver)
            i.name=name.first_name+' '+name.last_name
            i.link=User.objects.get(id=i.receiver).id
            i.user=name
        else:
            name=User.objects.get(id=i.sender)
            i.name=name.first_name+' '+name.last_name
            i.link=User.objects.get(id=i.sender).id
            i.user=name   

    return message_body

def load_more_msg(length,n):
    if(length==n):
        return True
    else:
        return False