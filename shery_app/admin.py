from django.contrib import admin
from .models import *

# Register your models here.
class Courses(admin.ModelAdmin):
    list_display = ['Image','Title','Description','Tutor','Topics','Price']
    list_editable=['Title','Description','Tutor','Topics','Price']

class CustomUserAdmin(admin.ModelAdmin):
    list_display=['is_superuser','username','first_name','last_name','email','phone','address','password']
    list_editable=['first_name','last_name','email','phone','address','password']

class EnrollmentAdmin(admin.ModelAdmin):
    list_display=['user','course']

class CartAdmin(admin.ModelAdmin):
    list_display=['user','created_at']

admin.site.register(course,Courses)
admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(Enrollement,EnrollmentAdmin)
admin.site.register(Cart,CartAdmin)

