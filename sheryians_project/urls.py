"""
URL configuration for sheryians_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from shery_app.views import *
urlpatterns = [
    path('admin/', admin.site.urls,name='admin'),
    path('home/',home,name='home'),
    path('add/',add,name='add'),
    path('add_course/',addCourse,name='add_course'),
    path('',welcome,name='welcome'),
    path('courses/',viewCourses,name='courses'),
    path('enrolled_courses/',viewEnrolledCourses,name='enrolled'),
    path('remove/<int:id>',remove,name='remove'),
    path('register/',register,name='register'),
    path('login/',Login,name='login'),
    path('logout/',logoutview,name='logout'),
    path('profile/',profile,name='profile'),
    path('display_profile',display_profile,name='display_profile'),
    path('course_details/<int:id>',buyCourse,name='buy'),
    path('add_to_cart/<int:id>',addToCart,name='add2cart'),
    path('view_cart/',viewCart,name='view_cart'),
    path('remove_cart_item/<int:id>',removeCartItem,name='remove_cart_item'),
    path('increase_quantity/<int:id>',increaseQuantity,name='increase_quantity'),
    path('decrease_quantity/<int:id>',decreaseQuantity,name='decrease_quantity'),
    path('new_enroll/<int:id>',enrollACourse,name='enroll'),
    path('admin_access/',viewAdmin,name='admin_access'),
    path('update_course/<int:id>',update,name='update_course'),
    path('movies/',movies,name='movies'),
    

]

urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_DIR)

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)