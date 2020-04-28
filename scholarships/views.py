from django.shortcuts import render
from django.http import HttpResponse
from scholarships.models import Scholarship

def scholarship_list(request):	
	scholarships = Scholarship.objects.all()
	return render(request, 'scholarships/scholarship_list.html', { 'scholarships': scholarships })

def scholarship_details(request,slug):
    scholarship = Scholarship.objects.get(slug=slug)
    return render(request, 'scholarships/scholarship_details.html', { 'scholarship': scholarship })