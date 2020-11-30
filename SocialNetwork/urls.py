"""SocialNetwork URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.http import JsonResponse
from django.conf.urls.static import static
from django.conf import settings
from . import views
from . import apiviews
from django.shortcuts import HttpResponse,redirect
import os
from  . import settings as s
from stories.models import *
from Friends.models import *
from django.core.files.storage import FileSystemStorage

def check(request):
    if request.method=='POST':
        try:
            profile=Profile.objects.get(user=request.user)
        except:
            profile=Profile()
            profile.user=request.user
        
        profile.profile_picture=request.FILES['photo']
        profile.save()
        post=Post()
        post.body=request.POST['status']
        post.user=request.user
        post.storytype=" updated profile picture "
        post.save()
        postimage=PostImage()
        postimage.url=profile.profile_picture
        postimage.post=post
        postimage.save()
        add_user_to_post(post,request.user)
        returndata={
            "imageid":postimage.id,
            "id":post.id,
            "name":request.user.first_name+" "+request.user.last_name,
            "date":post.date,
            "picture":str(postimage.url),
            "status":post.body
        }
        return JsonResponse(returndata)
 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/',views.signup),
    path('username_validate/',views.username_validate),
    path('login/',views.login_view),
    path('',include('stories.urls')),
    path('logout/',views.log_out),
    path('stories/',include('stories.urls')),
    path('messages/',include('message.urls')),
    path('profile/',include('Friends.urls')),
    path('search/',views.search),
    path('api/like/<int:id>/',apiviews.like),
    path('api/like/getlike/<int:id>/',apiviews.getlike),
    path('api/stories/comment/<int:id>/',apiviews.comment),
    path('update_pp/',check),
    path('api/messagecheck/',apiviews.messagecheck),
    path("api/stories/",apiviews.stories),
    path("api/get_notification",apiviews.get_notification,name="notifications"),
    path('', include('pwa.urls'))

    
]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)