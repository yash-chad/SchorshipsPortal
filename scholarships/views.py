from django.shortcuts import render
from django.http import HttpResponse
from scholarships.models import Scholarship
#Text Reading
from django.http import HttpResponse
import pytesseract as tess
from PIL import Image
import re


def scholarship_list(request):
    scholarships = Scholarship.objects.all()
    return render(request, 'scholarships/all.html', { 'scholarships': scholarships })

def scholarship_details(request,slug):
    scholarships = Scholarship.objects.all()
    scholarship = Scholarship.objects.get(slug=slug)
    return render(request, 'scholarships/detail.html', { 'scholarship': scholarship , 'scholarships': scholarships})


# The values scanned form the user's resume/marksheet are stored in this globaldata dic
globaldata ={"education" : ['computer','Computer']}

def specific(request):
	scholarships = Scholarship.objects.all()
	snew = []
	# Filtering for scholarships that match the user's qualification
	for obj in scholarships:
		for item in globaldata["education"]:
			if(obj.domain.lower().find(item)!=-1):
				snew.append(obj)
				break
	print(snew)
	if len(globaldata['education']) == 0:
		return render(request, 'scholarships/all.html', { 'scholarships': scholarships })
	else:
		return render(request, 'scholarships/specific.html', { 'scholarship': snew[0] , 'scholarships': snew})



# Text detection
def profile_page(request):
	tess.pytesseract.tesseract_cmd = r'C:\Users\HP\AppData\Local\Tesseract-OCR\tesseract.exe'
	img = Image.open('media/res.png')
	text = tess.image_to_string(img)
	lines = [el.strip().lower() for el in text.split('\n') if len(el.strip()) > 0]
	text = ' '.join(lines)
	# print(text)
	phone = None
	pattern = re.compile(r'(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}')
	m = re.finditer(pattern, text)
	for match in m:
		phone = match.group(0)
	print(phone)

	email = None
	pattern = re.compile(r'(\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+)')
	m = re.finditer(pattern, text)
	for match in m:
		email = match.group(0)
	print(email)

	education = []
	pattern = re.compile(r"(be|me|bsc|msc|btech|ba|ma|bachelor|bachelor's degree|master|master's degree|doctorate|computer|arts|commerce|law|engineering|master|humanities|fine arts|medical)\s?(of|in)\s?(\w+)")
	m = re.finditer(pattern, text)
	for match in m:
		education.append(match.group(3))
	print(education)

	scores = []
	pattern = re.compile(r'(cgpa|c.g.p.a.)\s*(\d+.?\d+)')
	m = re.finditer(pattern, text)
	for match in m:
		scores.append(match.group(2))
	pattern = re.compile(r'(\d+.?\d+)%')
	m = re.finditer(pattern, text)
	for match in m:
		scores.append(match.group(1))
	pattern = re.compile(r'(\d+.?\d+)(/\d+.?\d+)?\s*(cgpa|c.g.p.a.)')
	m = re.finditer(pattern, text)
	for match in m:
		scores.append(match.group(1))

	print(scores)
	globaldata["scores"] = scores
	globaldata["education"] = education
	print(globaldata)
	return render(request,'scholarships/profile.html',{'phone':phone,'email':email,'education':education,'scores':scores})




from django.shortcuts import render, redirect
from .models import Images
from .forms import ImagesForm

def home_view(request):
    context = {}
    if request.method == "POST":
        form = ImagesForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            img = form.cleaned_data.get("img")
            obj = Images.objects.create(
                                 name = name,
                                 img = img
                                 )
            obj.save()
            return redirect('scholarships:profile_page')
    else:
        form = ImagesForm()
    context['form']= form
    return render(request, "resume.html", context)
