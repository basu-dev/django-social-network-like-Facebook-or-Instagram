from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
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
        return User.objects.get(id=self.sender).username
    #for receiver's name in messanger
    def get_receiver_name(self):
        return User.objects.get(id=self.receiver).username


def get_message_with(u_id,id):
    messages = Message.objects.filter(Q(sender=u_id)|Q(receiver=u_id)).filter(Q(sender=id)|Q(receiver=id)).exclude(Q(del_by_sender = u_id)|Q(del_by_receiver=u_id))
    return messages
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
