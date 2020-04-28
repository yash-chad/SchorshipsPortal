from django.shortcuts import render,redirect
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.models import User
from django.contrib.auth import login,logout
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .forms import SignUpForm
from .tokens import account_activation_token
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Create your views here.
# def signup_view(request):
#     if request.method=='POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user=form.save()
#             #log user in
#             login(request,user)
#             return redirect('scholarships:scholarship_list')
#     else:
#         form = UserCreationForm()
#     return render(request,'accounts/signup.html',{'form':form})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # user.is_active = False
            user.save()
            login(request, user)
            return redirect('scholarships:scholarship_list')        
    else:
        form =  SignUpForm()
    return render(request,'accounts/signup.html',{'form':form})


def login_view(request):
    if request.method=='POST':
        form=AuthenticationForm(data=request.POST)
        if form.is_valid():
            #login
            user=form.get_user()
            login(request,user)
            if 'next' in request.POST :
                return redirect(request.POST.get('next'))
            else:
                return redirect('scholarships:scholarship_list')

    else:
        form=AuthenticationForm()

    return render(request,'accounts/login.html',{'form':form})


def logout_view(request):
    if request.method=='POST':
        logout(request)
        return redirect('scholarships:scholarship_list')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return render(request,'accounts/sent.html')
        # return redirect('scholarships:scholarship_list')
        # return redirect('home')
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


# iamawesome12345