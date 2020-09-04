from django.urls import path
from . import views
from . import apiviews

urlpatterns=[
    path('update_profile/',views.update_profile),
    path('my_profile/',views.profile),
    path('accept/<int:id>/',views.accept_request),
    path('deny/<int:id>/',views.deny_request),
    path('send_request/<int:id>/',views.send_request),
    path('<str:username>/',views.user_profile),
    path('unfriend/<int:id>/',views.unfriend),
    path('api/delete_story/<int:id>/',apiviews.delete),
    path('api/fetch_friends',apiviews.fetch_friends),
    path("api/get_profile_stories",views.get_profile_stories),
    path("api/friend_requests",views.get_friend_requests),
    path("api/sent_requests",views.get_sent_requests),
    path("api/friend_suggestions",views.get_friend_suggestions),
    path("api/get_profile_stories/<str:username>/",views.get_user_profile_stories),
    path("api/get_more_profile_stories/<int:id>/<int:fid>",views.get_more_profile_stories),
    path("api/get_more_profile_stories/<str:username>/<int:id>/<int:fid>",views.get_more_user_profile_stories),
]