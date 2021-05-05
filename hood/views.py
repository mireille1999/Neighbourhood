from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import *
from django.http import HttpResponse, Http404 
from .forms import BusinessForm,PostsForm,NewUserForm,notificationsForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib import messages
import datetime as datetime
import json
from django.db.models import Q
 

# Create your views here.
def index(request):
    hoods = Neighbourhood.objects.all()
    
    return render(request,'index.html',{"hoods":hoods})


@login_required(login_url='/accounts/login/')
def single_hood(request,location):
 
    location = Neighbourhood.objects.get(name=location) 
    print(location.id)
    businesses = Business.get_location_businesses(location.id) 
    posts = Posts.objects.filter(id=location.id) 
    print(posts)
   
    business_form = BusinessForm(request.POST)
    if request.method == 'POST':
        if business_form.is_valid():
            business = business_form.save(commit=False)
            business.user = request.user
            business.location = location
            business.save()
        return redirect('single_hood',location)
    
    else:
        business_form = BusinessForm()
        
    
    posts_form = PostsForm(request.POST)
    if request.method == 'POST':
        if posts_form.is_valid():
            form = posts_form.save(commit=False)
            form.user = request.user
            form.location = location
            form.save_post()
        return redirect('single_hood',location)
    
    else:
        posts_form = PostsForm()  
        
    context = {"location":location,
               "businesses":businesses,
               'business_form':business_form,
               "posts_form":posts_form,
                "posts":posts,
                }
    
    
    return render(request,'hood.html',context) 



@login_required(login_url='/accounts/login/')
def profile(request):
    profile = request.user
    try:
        profile_details = Profile.get_by_id(profile.id)
    except:
        profile_details = Profile.filter_by_id(profile.id)
    businesses = Business.get_profile_businesses(profile.id)
   
   
    business_form = BusinessForm(request.POST)
    if request.method == 'POST':
        if business_form.is_valid():
            business = business_form.save(commit=False)
            business.user = request.user
            business.location = location
            business.save()
        return redirect('single_hood',location)
    
    else:
        business_form = BusinessForm()
    
    return render(request, 'profile.html',{"profile":profile,"profile_details":profile_details,"businesses":businesses, 'business_form':business_form,}) 
    

@login_required(login_url='/accounts/login/')
def search_results(request):
    if 'business' in request.GET and request.GET['business']:
        search_term = request.GET.get("business")
        searched_businesses = Business.search_by_business(search_term)
        
        message = f'{search_term}'
        
        return render(request,'search.html',{"message":message,"businesses":searched_businesses})
    
    else:
        message = "You haven't searched for any term"
        return render(request,'search.html',{"message":message,"businesses":searched_businesses})


def logout_request(request):
	logout(request)
	return redirect("index")

def signup(request):
    signup_form= NewUserForm()
    if request.method == "POST":
        form = NewUserForm(request.POST)
        print(form)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
    return render(request, 'registration/registration_form.html', {'form': signup_form})

def login_request(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("index")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")

    return render(request=request, template_name="registration/login.html", context={"form":form})

@login_required(login_url='/accounts/login/')
def notification(request):
    current_user = request.user
    profile = Profile.objects.get(user=current_user)
    all_notifications = notifications.objects.filter(neighbourhood=profile.neighbourhood)

    return render(request, 'notifications.html', {"notifications":all_notifications})

@login_required(login_url='/accounts/login/')
def health(request):
    current_user = request.user
    profile = Profile.objects.get(user=current_user)
    healthservices = Health.objects.filter(neighbourhood=profile.neighbourhood)

    return render(request, 'health.html', {"healthservices":healthservices})

@login_required(login_url='/accounts/login/')
def authorities(request):
    current_user=request.user
    profile=Profile.objects.get(user=current_user)
    authorities=Authorities.objects.filter(neighbourhood=profile.neighbourhood)

    return render(request, 'authorities.html', {"authorities":authorities})


@login_required(login_url='/accounts/login/')
def new_notification(request):
    current_user = request.user
    profile = Profile.objects.get(user = current_user)

    if request.method == "POST":
        form = notificationsForm(request.POST, request.FILES)
        if form.is_valid():
            notification = form.save(commit=False)
            notification.author = current_user
            notification.neighbourhood = profile.neighbourhood
            notification.save()

            if notification.priority == 'High Priority':
                send_priority_email(profile.name, profile.email, notification.title, notification.notification, notification.author, notification.neighbourhood)

        return HttpResponseRedirect('/notifications')

    else:
        form = notificationsForm()

    return render(request, 'notifications_form.html', {"form":form})