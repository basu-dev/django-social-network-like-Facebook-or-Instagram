from django.shortcuts import render,redirect,HttpResponse
from . import urls
from .models import *
from message.models import *
from django.contrib.auth.decorators import login_required
from Friends.models import *
from django.http import JsonResponse

@login_required(login_url='/login/')
def storyline(request):
    if(request.is_ajax):
        return render(request,'storyline.html',{'page_title':'Home-Raven'})

@login_required(login_url='/login/')
def storydetail(request,id):
    try:
        story=get_single_story(request,id)
    except:
        story=None
        request.message="The story was not found. It might have  been deleted by the user."
        
    return render(request,"storydetail.html",{"story":story})

@login_required(login_url="/login")
def updatestory(request):
    if request.method=='POST':
        imageId=request.POST['imageId']
        storyId=request.POST['storyId']
        post=Post.objects.get(id=storyId)
        if(request.user==post.user):            
            post.body=request.POST['status']
            post.save()
            try:
                image=PostImage.objects.get(id=imageId)
                try:
                    image.url=request.FILES['image']
                    image.save()
                except:
                    pass
            except:
                try:
                    image=PostImage()
                    image.url=request.FILES['image']
                    image.post=post
                    image.save()
                except:
                    pass
            return JsonResponse({"success":True,
                "id":post.id,
                "imageid":image.id,
                "status":post.body,
                "picture":str(image.url)
            })
        
        else:
            return JsonResponse({"success":False})
    return JsonResponse({"success":False})
@login_required(login_url="/login")
def get_some_more_stories(request,id,fid):
    result=get_more_stories_all(request,request.user,id,fid)
    stories=result[0]
    lastid=result[1]
    firstid=result[2]
    request.loadmore=load_more(lastid)
    return render(request,"../templates/shared/stories.html",{"stories":stories,"lastid":lastid,"firstid":firstid})
@login_required(login_url="/login")
def get_stories(request):
    result=get_stories_all_friends(request,request.user)
    stories=result[0]
    lastid=result[1]
    firstid=result[2]
    request.loadmore=load_more(lastid)
    return render(request,"../templates/shared/stories.html",{"stories":stories,"lastid":lastid,"firstid":firstid})
@login_required(login_url="/login")
def loadMessanger(request):
    friend_list=[]
    messages=[]
    message_body=[]
    friend_list = get_all_friends_user(request.user.id)
    messages=get_message_with(request.user.id,3)[0] 
    receiver=User.objects.get(id=1).first_name 
    for  i in messages:
        i.sender=User.objects.get(id=i.sender)
    message_body=get_last_message_body_homepage(request.user.id,friend_list)
    if(message_body==[]):
        request.nomessage=True
    return render(request,"../templates/shared/storyline-messagebox.html",{
    'receiver':receiver,
    'message_body':message_body,
    'messages':messages,
    })