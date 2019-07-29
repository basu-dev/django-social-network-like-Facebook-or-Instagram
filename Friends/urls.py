from django.urls import path
from . import views
from . import apiviews

urlpatterns=[
    path('update_profile/',views.update_profile),
    path('my_profile/',views.profile),
    path('delete/<int:id>/',views.delete),
    path('message/<int:id>/',views.profile),
    path('accept/<int:id>/',views.accept_request),
    path('deny/<int:id>/',views.deny_request),
    path('send_request/<int:id>/',views.send_request),
    path('<str:username>/',views.user_profile),
    path('unfriend/<int:id>/',views.unfriend),
    path('api/delete_story/<int:id>/',apiviews.delete),
    



]