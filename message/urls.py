from django.urls import path
from . import views
from . import apiviews
urlpatterns=[
    path('<int:id>/',views.message),
    path('api/<int:id>/',apiviews.send_message)
]