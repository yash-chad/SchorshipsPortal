from django.shortcuts import render
from django.http import HttpResponse
from scholarships.models import Scholarship

<<<<<<< HEAD
def scholarship_list(request):	
	scholarships = Scholarship.objects.all()
	return render(request, 'scholarships/scholarship_list.html', { 'scholarships': scholarships })
=======
def scholarship_list(request):
    scholarships = Scholarship.objects.all()
    return render(request, 'scholarships/all.html', { 'scholarships': scholarships })
>>>>>>> b8a24efaf4c9bf1402e62f528cffc4e75a7388fc

def scholarship_details(request,slug):
    scholarships = Scholarship.objects.all()
    scholarship = Scholarship.objects.get(slug=slug)
    return render(request, 'scholarships/detail.html', { 'scholarship': scholarship , 'scholarships': scholarships})


# def profile_page(request):
#     return render(request, 'scholarships/profile.html')

# def edit_profile(request):
#     return render(request, 'scholarships/edit_profile.html')