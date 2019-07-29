from django.shortcuts import render,redirect,HttpResponse
from .models import *
from django.contrib.auth.decorators import login_required
from stories.models import *
from Friends.models import *
# Create your views here.
@login_required(login_url='/login/')
def message(request,id):
    if request.method=='POST':
        message=request.POST['message']
        if message:
            new_message=Message()
            new_message.sender =request.user.id
            new_message.receiver =id
            new_message.body = message
            new_message.save()
            return redirect('/messages/'+str(id)+'/')
    else:
        friend_list=[]
        stories=[]
        messages=[]
        friends = get_all_friends(request.user.id)
        for i in friends:
            if i.sender is not request.user.id:
                friend_list+=User.objects.filter(id=i.sender)
            else:
                friend_list+=User.objects.filter(id=i.receiver)
        for i in friend_list:
            stories+=Post.objects.filter(user=i).order_by('date')
        for story in stories:
            story.comment=get_comment(story.id)
        for story in stories:
            story.like = Like.objects.filter(post = story)
        messages+=get_message_with(request.user.id,id)

        for  i in messages:
            if i.seen is False and i.receiver is request.user.id:
                i.seen=True
                i.save()
            i.sender=User.objects.get(id=i.sender)
        receiver=User.objects.get(id=id)
        request.notification=get_last_ten(request.user)
        return render(request,'message.html',{'receiver':receiver,'page_title':'Home-Message','friend_list':friend_list,'stories':stories,'messages':messages})
