from django.shortcuts import render,redirect,HttpResponse
from .models import *
from django.contrib.auth.models import User
from stories.models import *
from Friends.models import *
import random
from django.contrib.auth.decorators import login_required
from django.core.signals import request_finished
from django.db.models.signals import post_save
from django.http import JsonResponse

@login_required(login_url='/login/')
def profile(request):
    # if request.is_ajax:
        if request.method=='POST':
            new_story=Post()
            if(len(request.POST['add_story'])== 0):
                try:
                    url=request.FILES['images']
                except:
                    return JsonResponse({"failed":True})
            new_story.body = request.POST['add_story']
            new_story.user = request.user
            new_story.save()
            try:
                newimage=PostImage()
                newimage.url=request.FILES['images']
                newimage.post=new_story
                newimage.save()
            except:
                pass
            addusertopost=add_user_to_post(new_story,request.user)
            if(addusertopost):
                returndata={
                "imageid":newimage.id,
                "id":new_story.id,
                "name":request.user.first_name+" "+request.user.last_name,
                "date":new_story.date,
                "picture":str(newimage.url),
                "status":new_story.body
                }
                return JsonResponse(returndata)
            else:
                return JsonResponse({"failed":True})
        else:
            profile = User.objects.get(id=request.user.id)
            # random.suffle(friend_suggestion)
            request.isprofile=True
            return render(request,'profile.html',
            {
            'profile':profile,
            'page_title':request.user.first_name+' '+request.user.last_name})

@login_required(login_url='/login/')
def accept_request(request,id):
    if request.method =='POST':
        new_friend=Friend()
        new_friend.sender= id
        new_friend.receiver =request.user.id
        userassigned=assign_users_to_my_post(request.user,User.objects.get(id=id))
        new_friend.save()
        if(userassigned==True):
            user=User.objects.get(id = id)
            set_notification(user,request.user.first_name +' '+ request.user.last_name + ' accepted your Connect Request.',0,'route("profile/'+request.user.username+'")')
            friend_request = Friend_request.objects.filter(sender = id).get(receiver=request.user.id)
            friend_request.delete()
            return render(request,"../templates/buttons/disconnectbtn.html",{"user":user})
        else:
            return HttpResponse("Some Errors Processing")
@login_required(login_url='/login/')
def deny_request(request,id):
    try:
        friend_request_received = Friend_request.objects.filter(sender = id).get(receiver=request.user.id)
        friend_request_received.delete()
        return render(request,"../templates/buttons/connectbtn.html",{"id":id})
    except:
        pass
    try:
        friend_request_received = Friend_request.objects.filter(sender = request.user.id).get(receiver=id)
        friend_request_received.delete()
        return render(request,"../templates/buttons/connectbtn.html",{"id":id})
    except:
        pass
    return False
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
                set_notification(user,request.user.first_name+' '+request.user.last_name +' sent you Connect Request.',0,'getFriendRequests()')
                return render(request,"../templates/buttons/cancelbtn.html",{"id":id})
            else:
                return False
        else:
            return False
    else:
        return False
@login_required(login_url='/login/')
def user_profile(request,username):
    if(username==request.user.username):
        return JsonResponse({"isuser":True})
    try:
        user = User.objects.get(username = username)
        user=attach_status(request.user.id,user)
        status=get_friendship_status(request.user.id,user.id)
        return render(request,'friend_profile.html',
        {'user':user
        ,'page_title':user.first_name+' '+user.last_name,
        })
    except:
        user = 0
        return redirect('/profile/my_profile/')
@login_required(login_url='/login/')
def unfriend(request,id):
    remove_users_from_my_post(request,User.objects.get(id=id))

    
    try:
        friend=Friend.objects.filter(Q(sender=request.user.id) |Q(sender=id)).filter(Q(receiver=request.user.id) |Q(receiver=id)).get()
        if friend:
            friend.delete()
            return render(request,"../templates/buttons/connectbtn.html",{"id":id})
        else:
            return False
    except:
        return False     
    return False
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
            profile.contact_no=contact_no
        if bio:
            profile.bio=bio
        if job:
            profile.job=job
        profile.save()
        user.save()
        return JsonResponse({'success':True})
@login_required(login_url="/login")
def get_profile_stories(request):
    result=get_stories_user(request,request.user)
    stories=result[0]
    lastid=result[1]
    firstid=result[2]
    if(lastid!=0):
        request.show_more=True
    request.isprofile=True
    request.loadmore=load_more(lastid)
    return render(request
    ,"../templates/shared/profile-stories.html"
    ,{"stories":stories,
    "lastid":lastid,
    "firstid":firstid
    })
@login_required(login_url="/login")
def get_more_profile_stories(request,id,fid):
    result=get_more_stories_user(request,request.user,id,fid)
    stories=result[0]
    lastid=result[1]
    if(lastid!=0):
        request.show_more=True
    request.isprofile=True
    request.loadmore=load_more(lastid)
    return render(request
    ,"../templates/shared/profile-stories.html"
    ,{"stories":stories
    ,"lastid":lastid
    })
@login_required(login_url="/login")
def get_friend_requests(request):
    request_list=get_friend_request_list(request.user.id)
    return render(request,
    "../templates/search.html",
    {'users':request_list
    }
    )
@login_required(login_url="/login")
def get_sent_requests(request):
    request_list=get_sent_request_list(request.user.id)
    return render(request,
    "../templates/search.html",
    {'users':request_list
    }
    )
@login_required(login_url="/login")
def get_friend_suggestions(request):
    friend_suggestion=get_friend_suggestion(request.user.id,request.user)
    return render(request,
    "../templates/search.html",
    {'users':friend_suggestion
    }
    )

@login_required(login_url="/login")
def get_user_profile_stories(request,username):
    user=User.objects.get(username=username)
    result=get_stories_user(request,user.id)
    stories=result[0]
    lastid=result[1]
    firstid=result[2]
    request.loadmore=load_more(lastid)  
    return render(request
    ,"../templates/shared/profile-stories.html"
    ,{"stories":stories
    ,"lastid":lastid,
    "firstid":firstid
    })
@login_required(login_url="/login")
def get_more_user_profile_stories(request,username,id,fid):
    user=User.objects.get(username=username)
    result=get_more_stories_user(request,user.id,id,fid)
    stories=result[0]
    lastid=result[1]
    request.loadmore=load_more(lastid)
    return render(request
    ,"../templates/shared/profile-stories.html"
    ,{"stories":stories
    ,"lastid":lastid
    })