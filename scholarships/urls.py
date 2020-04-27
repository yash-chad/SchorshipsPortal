from django.urls import path
from . import views
app_name = 'scholarships'

urlpatterns = [
    path('',views.scholarship_list,name='scholarship_list'),       #The urls can now be identified by this name field!
    path('profile/',views.profile,name='profile'),
    path('edit/',views.edit, name = 'edit'),
    path('<slug:slug>/',views.scholarship_details,name='scholarship_details'),
]
