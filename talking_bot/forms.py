from .models import Images
from django.forms import ModelForm

class  ImagesForm(ModelForm):
	class Meta:
		model = Images
		fields = ['name', 'img']
