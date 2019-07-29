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
from django.conf.urls.static import static
from django.conf import settings
from . import views
from . import apiviews
from django.shortcuts import HttpResponse,redirect
import os
from  . import settings as s
from Friends.models import Profile
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
        fss=FileSystemStorage()
        fss.save("user-profile/"+request.FILES['photo'].name,request.FILES['photo'])
        return redirect('/profile/my_profile')
 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/',views.signup),
    path('login/',views.login_view),
    path('',include('stories.urls')),
    path('logout/',views.log_out),
    path('stories/',include('stories.urls')),
    path('messages/',include('message.urls')),
    path('profile/',include('Friends.urls')),
    path('search/',views.search),
    path('api/like/<int:id>/',apiviews.like),
    path('api/stories/comment/<int:id>/',apiviews.comment),
    path('update_pp/',check),
    path('api/messagecheck/',apiviews.messagecheck),
    
]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)