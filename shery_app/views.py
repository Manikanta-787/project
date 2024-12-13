from django.shortcuts import render,redirect,HttpResponse
from .models import *
from .forms import course_form,RegisterForm,LoginForm,UserProfileForm,ProfileForm
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from requests import get
from bs4 import BeautifulSoup

# Create your views here.
def home(request):
    return render(request,'home.html')

def add(request):
    query_list = course.objects.all()
    length=len(query_list)
    required_object=query_list[length-1] #latest row
    topics_data=required_object.Topics
    topics_list=topics_data['fruits']
    return render(request,'updated.html',{'row':required_object,'Topics':topics_list})

def addCourse(request):
    f=course_form()
    if request.method == 'POST':
        form=course_form(request.POST,request.FILES)
        if form.is_valid():
                form.save()
                query_list = course.objects.all()
                return render(request,'admin.html',{'data':query_list})
    return render(request,'form.html',{'form':f})


def welcome(request):
        user=request.user
        if user.is_authenticated:
            cart_obj=Cart.objects.filter(user=user)
            if cart_obj:
                cart_items=CartItem.objects.filter(cart=cart_obj[0])
                already_present_course_ids=[]
                for i in cart_items:
                    already_present_course_ids.append(i.course.id)

            enrolled_items=Enrollement.objects.filter(user=user)
            if enrolled_items:  
                enrolled_courses_ids=[]

                for i in enrolled_items:
                    enrolled_courses_ids.append(i.course.id)
            x=request.user
            if cart_obj and enrolled_items:     
                query_list = course.objects.all()
                return render(request,'welcome.html',{'data':query_list,'user':x,'enrolled_course_ids':enrolled_courses_ids,'already_present_course_ids':already_present_course_ids})
            elif(cart_obj):
                query_list = course.objects.all()
                return render(request,'welcome.html',{'data':query_list,'user':x,'already_present_course_ids':already_present_course_ids})
            elif(enrolled_items):
                query_list = course.objects.all()
                return render(request,'welcome.html',{'data':query_list,'user':x,'enrolled_course_ids':enrolled_courses_ids})
        x=request.user
        query_list = course.objects.all()
        return render(request,'welcome.html',{'data':query_list,'user':x})

def remove(request,id):
       r_object=course.objects.get(id=id)
       r_object.delete()
       query_list = course.objects.all()
       return render(request,'welcome.html',{'data':query_list})

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = CustomUser.objects.filter(username__iexact=username)
        if user.exists():
            messages.error(request, 'User with this username already exists.')
            return redirect(reverse('register')) 
        form = RegisterForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()  
            messages.success(request, 'Registration successful. Please log in.')
            return redirect(reverse('welcome')) 
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    form = RegisterForm()
    return render(request, 'register.html', {'form': form})




def Login(request):
    if request.method == 'POST':
        form=LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user :
                    login(request, user)
                    messages.success(request, f'Welcome back, {username}!')
                    return redirect('welcome')  # Redirect to a home page or other page after login
            else:
                    messages.error(request, 'Invalid username or password.')
        
        
    form = LoginForm()
    return render(request, 'login.html', {'form': form})
def logoutview(request):
      logout(request)
      return redirect('welcome')
# @login_required(login_url='login')
def profile(request):
      if request.method == "POST":
            form = UserProfileForm(request.POST,request.FILES)
            if form.is_valid():
                  form.save()
                  return HttpResponse('<h1 style="text-align:center;color:goldenrod;background-color:yellow">Completed Profile Successfully</h1>')
      data=UserProfileForm()
      return render(request,'profile.html',{'form':data})


def display_profile(request):
    user=request.user
    profile_data=CustomUser.objects.get(id=user.id)
    form=ProfileForm()
    if request.method == 'POST':
         form = ProfileForm(request.POST)
         if form.is_valid():
              user.username=form.cleaned_data['username']
              user.first_name=form.cleaned_data['first_name']
              user.last_name=form.cleaned_data['last_name']
              user.email=form.cleaned_data['email']
              user.address=form.cleaned_data['address']
              user.phone=form.cleaned_data['phone']
              user.save()
              return redirect('display_profile')
    return render(request,'display_profile.html',{'profile_data':profile_data})


def buyCourse(request,id):
      course_data=course.objects.get(id=id)
      return render(request,'buy.html',{'data':course_data})

def addToCart(request,id):
      course_id=id
      course_obj=course.objects.get(id=course_id)
      cart_obj,created=Cart.objects.get_or_create(user_id=request.user.id)
      
      cart_item_obj,create=CartItem.objects.get_or_create(cart=cart_obj,course=course_obj)
      cart_item_obj.quantity += 1
      cart_item_obj.save()

      return redirect('welcome')

def viewCart(request):
    cart_obj,created=Cart.objects.get_or_create(user=request.user)
    cart_items=CartItem.objects.filter(cart=cart_obj)
    total_cart_items=len(cart_items)
    return render(request,'view_cart.html',{'cart_items':cart_items , 'total_price':cart_obj.total_price(),'total_no_of_items':total_cart_items}) 

def increaseQuantity(request,id):
    course_id=id
    course_obj=course.objects.get(id=course_id)
    cart_item_id=request.user.id
    cart_obj=Cart.objects.get(user=request.user)
    cart_item=CartItem.objects.get(cart=cart_obj,course=course_obj)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('view_cart')

def decreaseQuantity(request,id):
    course_id=id
    course_obj=course.objects.get(id=course_id)
    cart_item_id=request.user.id
    cart_obj=Cart.objects.get(user=request.user)
    cart_item=CartItem.objects.get(cart=cart_obj,course=course_obj)
    cart_item.quantity -= 1
    cart_item.save()
    return redirect('view_cart')
def viewCourses(request):
       user=request.user
       if user.is_authenticated:
            cart_obj=Cart.objects.get(user=user)
            cart_items=CartItem.objects.filter(cart=cart_obj)
            already_present_course_ids=[]
            for i in cart_items:
                already_present_course_ids.append(i.course.id)

            enrolled_items=Enrollement.objects.filter(user=user)
            enrolled_courses_ids=[]

            for i in enrolled_items:
                enrolled_courses_ids.append(i.course.id)

            query_list = course.objects.all()
            return render(request,'courses.html',{'data':query_list,'user':user,'enrolled_course_ids':enrolled_courses_ids,'already_present_course_ids':already_present_course_ids})
       query_list = course.objects.all()
       return render(request,'courses.html',{'data':query_list,'user':user})
def removeCartItem(request,id):
      course_id=id
      course_obj=course.objects.get(id=course_id)
      user_object=request.user
      cart_item_obj=CartItem.objects.filter(course=course_obj)
      cart_item_obj.delete()
      return redirect('view_cart')
      
def viewEnrolledCourses(request):
     user=request.user
     enrolled_course_list=Enrollement.objects.filter(user=user)
     total_courses=len(enrolled_course_list)
     return render(request,'enrolled_courses.html',{'courses':enrolled_course_list,'count':total_courses})
def enrollACourse(request,id):
     course_id=id
     course_obj=course.objects.get(id=course_id)
     is_enrolled=Enrollement.objects.filter(course=course_obj,user=request.user)
     if is_enrolled:
          return redirect('enrolled')
     user=request.user
     enroll_obj=Enrollement.objects.create(user=user,course=course_obj)
     enroll_obj.save()
     return redirect('enrolled')

def viewAdmin(request):
     query_list = course.objects.all()
     return render(request,'admin.html',{'data':query_list})

def update(request,id):
     course_obj=course.objects.get(id=id)
     if request.method == 'POST':
          form=course_form(request.POST,request.FILES,instance=course_obj)
          if form.is_valid():
               form.save()
               return redirect('admin_access')
          else:
               print('no')
     form=course_form(instance=course_obj)
     return render(request,'update_course.html',{'course':course_obj,'form':form})
    
def movies(request):
    url='https://ibomma.movie/'
    response=get(url)
    soup=BeautifulSoup(response.text,'html.parser')
    movie_details=[]
    movie_card_containers=soup.find_all('div',class_='gb-grid-wrapper')
    movie_cards=[]
    for card_container in movie_card_containers:
        cards=card_container.find_all('div',class_='gb-grid-column')
        movie_cards+=cards

    for card in movie_cards:
        card_details=dict()
        if card.find('p'):
            card_details['title']=card.find('p').text
        else:
            card_details['title']='Not Available'
        
        if card.find('img'):
            card_details['image']=card.find('img').get('data-src')
        else:
            card_details['image']='Not Available'
        
        if card.find('a'):
            card_details['source']=card.find('a').get('href')
        else:
            card_details['source']='#'

        if card.find('span'):
            card_details['year']=card.find('span').text
        else:
            card_details['year']='Not Available'
        
        movie_details.append(card_details)

    return render(request,'movies.html',{'movies':movie_details})

