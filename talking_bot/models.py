from django.db import models

# Create your models here.
class Conversation:
	id: int
	question: str
	answer: str

class Images(models.Model):
	name = models.CharField(max_length = 100, blank = True, null = True)
	img = models.ImageField()
	