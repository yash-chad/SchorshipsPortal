from django.db import models

# Create your models here.
class Conversation:
	id: int
	question: str
	answer: str