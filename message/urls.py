from django.urls import path
from . import views
from . import apiviews
urlpatterns=[
    
    path('api/<int:id>/',apiviews.send_message),
    path('api/get/<int:id>/',views.singleUserMsg),
    path("moremessages/<int:id>/<int:lastid>",views.get_more_message)
]