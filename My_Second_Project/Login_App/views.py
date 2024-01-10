from django.shortcuts import render
from Login_App.forms import UserForm, UserInfoForm
from Login_App.models import UserInfo
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse


# Create your views here.

def login_page(request):
    return render(request, 'Login_App/login.html', context={})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username= username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('Login_App:index'))
                # return render(request, 'Login_App/login.html', context={})
            else:
                return HttpResponse("Access is not active!!")
            
        else:
            return HttpResponse("Login details are Wrong!")

    else:
        # return render(request, 'Login_App/login.html', context={})
        return HttpResponseRedirect(reverse('Login_app:login'))


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('Login_App:index'))


def index(request):
    dict={}
    if request.user.is_authenticated:
        current_user = request.user
        user_id = current_user.id
        user_basic_info = User.objects.get(pk=user_id)
        user_more_info = UserInfo.objects.get(user__pk=user_id)

        # print (current_user.username)
        # print (current_user.email)
        # print(current_user.id)
        dict = {'user_basic_info':user_basic_info, 'user_more_info': user_more_info}

    return render(request, 'Login_App/index.html', context=dict)


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        user_info_form = UserInfoForm(data=request.POST)

        if user_form.is_valid() and user_info_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            user_info = user_info_form.save(commit=False)
            user_info.user = user

            if 'profile_pic' in request.FILES:
                user_info.profile_pic = request.FILES['profile_pic']
            
            user_info.save()

            registered = True

    else:
        user_form = UserForm()
        user_info_form = UserInfoForm()

    dict = {'user_form': user_form, 'user_info_form': user_info_form, 'registered': registered} 
    return render(request, 'Login_App/register.html', context=dict)








