from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Scholarship(models.Model):
    title =  models.CharField(max_length=100)
    slug = models.SlugField()
    body = models.TextField()
    postedOn = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField()
    criteria = models.IntegerField()
    domain = models.CharField(max_length=100)
    thumb = models.ImageField(default='default.jpg',blank=True)

    #This is what will be displayed in the admin and the shell while retriving
    def __str__(self):
        return self.title

    def snippet(self):
        return self.body[:100] + '...'

class Profile(models.Model):
    User = models.OneToOneField(User,on_delete=models.CASCADE)
    Resume = models.FileField(upload_to='media/docs/',default=None,null=True,blank=True)
    profile_img = models.ImageField(upload_to='images/', default="images/default.png")

    def __str__(self):
        return self.User.username
    


    
    
