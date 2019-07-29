from django.shortcuts import render,redirect
from . import urls
from .models import *
from message.models import *
from django.contrib.auth.decorators import login_required
from Friends.models import get_all_friends
@login_required(login_url='/login/')
def storyline(request):
    friend_list=[]
    stories=[]
    messages=[]
    message_body=[]
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
    messages+=get_message_with(request.user.id,3)
    for  i in messages:
        
        i.sender=User.objects.get(id=i.sender)
    receiver=User.objects.get(id=3).first_name 
    for i in friend_list:
       message_body+= get_last_message_with(request.user.id,i.id)
       

    #was error while applying if inside storylin so we used if inside views (gettin the name of our friend but not ours)
    for i in message_body:
        if i.sender==request.user.id:
            name=User.objects.get(id=i.receiver)
            i.name=name.first_name+' '+name.last_name
            i.link=User.objects.get(id=i.receiver).id
            i.user=name
        else:
            name=User.objects.get(id=i.sender)
            i.name=name.first_name+' '+name.last_name
            i.link=User.objects.get(id=i.sender).id
            i.user=name
    request.notification=get_last_ten(request.user)
    return render(request,'storyline.html',{'receiver':receiver,'message_body':message_body,'page_title':'Home-Raven','friend_list':friend_list,'stories':stories,'messages':messages})


@login_required(login_url='/login/')
def save_comment(request, id):
    if request.method=='POST':
        comment = request.POST['comment']
        new_cmt = Comment()
        new_cmt.body= comment
        new_cmt.user =  request.user
        new_cmt.post  = Post.objects.get(id = id)
        if comment:
            set_notification(new_cmt.post.user,request.user.username +' commented on your post :'+comment ,0,'/profile/')
            new_cmt.save()
        
        return redirect('/')
    else:
        return redirect('/')

@login_required(login_url='/login/')
def save_like(request, id):
    if request.method=='POST':
       post =Post.objects.get(id = id)
       try:
           like=Like.objects.filter(user=request.user).filter(post=post)
       except:
            like=0  
       if like:
           like.delete()
           try:
               link=request.POST['redirect_to']
           except:
                link=0
           if link:
                return redirect(link)
           else:
                return redirect('/')
       else:
            newlike=Like()
            newlike.user=request.user
            newlike.post=post
            newlike.like=True
            newlike.save()
            set_notification(post.user, request.user.first_name+' '+request.user.last_name +'liked your post.',0,'/profile/')
            return redirect('/')
    else:
        return redirect('/')        
