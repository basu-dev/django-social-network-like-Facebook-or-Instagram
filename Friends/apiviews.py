from stories.models import Post
from django.shortcuts import render,redirect,HttpResponse

from django.http import JsonResponse
from Friends.models import *

def delete(request,id):
    if request.method=='POST':
        story = Post.objects.get(id=id)
        story.delete()
        return JsonResponse({'success':"successful"})

def fetch_friends(request):
    friend_list=get_all_friends_user(request.user.id)
    return render(request,"../templates/shared/friends.html",{"friend_list":friend_list})

