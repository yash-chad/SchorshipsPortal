from django.db import models

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

from django.db import models

# Create your models here.
class Images(models.Model):
	name = models.CharField(max_length = 100, blank = True, null = True)
	img = models.ImageField()
	