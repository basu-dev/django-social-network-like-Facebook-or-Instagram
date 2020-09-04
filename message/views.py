from django.shortcuts import render,redirect,HttpResponse
from .models import *
from django.contrib.auth.decorators import login_required
from stories.models import *
from Friends.models import *

@login_required(login_url="/login")
def singleUserMsg(request,id):
    result=get_message_with(request.user.id,id)
    messages=result[0]
    request.lastid=result[1]
    request.loadmore=load_more(result[1])  
    for  i in messages:
        if i.seen is False and i.receiver is request.user.id:
                i.seen=True
                i.save()
        i.sender=User.objects.get(id=i.sender)
    request.loadmore=load_more_msg(len(messages),15)
    request.receiver=User.objects.get(id=id)
    
    return render(request,"../templates/shared/messagebox.html",{"messages":messages})
@login_required(login_url="/login")
def get_more_message(request,id,lastid):
    result=get_more_message_with(request.user.id,id,lastid)
    messages=result[0]
    request.lastid=result[1]
    request.loadmore=load_more(result[1])
    for  i in messages:
        if i.seen is False and i.receiver is request.user.id:
                i.seen=True
                i.save()
        i.sender=User.objects.get(id=i.sender)
    request.receiver=User.objects.get(id=id)
    request.loadmore=load_more_msg(len(messages),10)
    return render(request,"../templates/shared/messageupdate.html",{"messages":messages})
