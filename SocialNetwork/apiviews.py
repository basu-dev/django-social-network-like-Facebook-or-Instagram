from django.http import JsonResponse
from django.shortcuts import render,redirect,HttpResponse

from stories.models import *
from message.models import *


def like(request,id):
    if request.is_ajax:
        if request.method == 'POST':
            post=Post.objects.get(id= id)
            like=Like.objects.filter(post=post).filter(user=request.user)
            if like:
                like.delete()
                count=Like.objects.filter(post=post).count()
                truth='True'
                is_liked='Like'
            else:
                like=Like()
                like.user=request.user
                like.post=post
                like.like=True
                like.save()
                if(like.post.user.id is not request.user.id):
                    set_notification(like.post.user, request.user.first_name+' '+request.user.last_name +' liked your story.',0,'route("storydetail/'+str(post.id)+'")')
                count=Like.objects.filter(post=post).count()
                truth='False'
                is_liked='Liked'
            return JsonResponse({'count':count,'truth':truth,'is_liked':is_liked})

def comment(request,id):
    if request.method=='POST':
        comment = request.POST['comment']
        new_cmt = Comment()
        new_cmt.body= comment
        new_cmt.user =  request.user
        new_cmt.post  = Post.objects.get(id = id)
        if comment:
            new_cmt.save()
            if(new_cmt.post.user.id is not request.user.id):

                set_notification(new_cmt.post.user, request.user.first_name+' '+request.user.last_name +' commented on your story.',0,'route("storydetail/'+str(new_cmt.post.id)+'")')

            data={"comment":comment,
            "user":request.user.first_name+" "+request.user.last_name,
            "profile_picture":request.user.profile.profile_picture.url,
            "url":"/profile/"+request.user.username
            }
            return JsonResponse(data)

def messagecheck(request):
    new_message=Message_Notification.objects.filter(receiver=request.user.id)[0]
    user=User.objects.get(id=new_message.sender)
    u_id=request.user.id
    id=new_message.sender
    get_last_message=Message.objects.filter(Q(sender=u_id)|Q(receiver=u_id)).filter(Q(sender=id)|Q(receiver=id)).exclude(Q(del_by_sender = u_id)|Q(del_by_receiver=u_id)).filter(seen=False).last()
def stories(request):
    if request.is_ajax:
        post=Post.objects.get(id=2)
        image=PostImage()
        image.post=post
        image.url="/static/message.jpg/" 
        return JsonResponse({"st":"image"})

def get_notification(request):
    notifications=get_last_ten(request.user.id)
    return render(request,"shared/notification.html",{"notifications":notifications})
def getlike(request,id):
    likers=[]
    story=Post.objects.get(id=id)
    story.like=Like.objects.filter(post=story)
    for like in story.like:
        likers+=User.objects.filter(id=like.user.id)
    return render(request,"shared/likers.html",{"likers":likers})