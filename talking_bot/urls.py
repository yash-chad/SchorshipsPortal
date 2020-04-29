
from django.urls import path, include
from . import views
urlpatterns = [
    path('train', views.train, name="train"),
    path('home', views.home, name="home"),
    path('display', views.display, name="display")

]




