from django.urls import path
from . import views

urlpatterns=[
    path('',views.storyline),
    path("storydetail/<int:id>/",views.storydetail),
    path("updatestory",views.updatestory),
    path("get_stories/",views.get_stories),
    path("get_more_stories/<int:id>/<int:fid>",views.get_some_more_stories),
    path("messanger",views.loadMessanger)
]