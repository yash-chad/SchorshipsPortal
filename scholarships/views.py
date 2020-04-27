from django.shortcuts import render
from django.http import HttpResponse
from scholarships.models import Scholarship,Profile
from django.contrib.auth.decorators import login_required

# Create your views here.

def scholarship_list(request):
    scholarships = Scholarship.objects.all()
    return render(request, 'scholarships/all.html', { 'scholarships': scholarships })

def scholarship_details(request,slug):
    scholarships = Scholarship.objects.all()
    scholarship = Scholarship.objects.get(slug=slug)
    return render(request, 'scholarships/scholarship_details.html', { 'scholarship': scholarship })


def edit(request):
    pass

@login_required(login_url="/accounts/login/")
def profile(request):
    tempuser = request.user
    if Profile.objects.get(User=tempuser):
        profile = Profile.objects.get(User=tempuser)  
        return render(request,'scholarships/profile.html',{'user':tempuser,'profile':profile})
    else:
        return HttpResponse("Login to see your profile")
    

def edit(request):
    
    if request.user=='POST':
        User = request.user
        profile=Profile.objects.get(User=User)
        profile.User.username = request.GET.get('username')
        profile.User.email =request.GET.get('email')
        profile.User.first_name = request.GET.get('firstname')
        profile.User.last_name =request.GET.get('lastname') 
        profile.profile_img = request.FILES('pfp')
        profile.Resume = request.FILES('resume')
        profile.save()
        return redirect('scholarships:profile',{'profile':profile})
    else:
        user = request.user
        profile=Profile.objects.get(User=user)
        return render(request,'scholarships/edit_profile.html',{'profile':profile})
    

