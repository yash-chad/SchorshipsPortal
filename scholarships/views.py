from django.shortcuts import render
from django.http import HttpResponse
from scholarships.models import Scholarship,Profile
from django.contrib.auth.decorators import login_required

# Create your views here.

def scholarship_list(request):
    scholarships = Scholarship.objects.all()
    return render(request, 'scholarships/scholarship_list.html', { 'scholarships': scholarships })

def scholarship_details(request,slug):
    scholarship = Scholarship.objects.get(slug=slug)
    return render(request, 'scholarships/scholarship_details.html', { 'scholarship': scholarship })


def edit(request):
        return HttpResponse("Edit Profile")

@login_required(login_url="/accounts/login/")
def profile(request):
    tempuser = request.user
    if Profile.objects.get(User=tempuser):
        profile = Profile.objects.get(User=tempuser)  
        return render(request,'scholarships/profile.html',{'user':tempuser,'profile':profile})
    else:
        return HttpResponse("Create an account to see your profile")
    

