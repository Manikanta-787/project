from django import forms
from .models import course,CustomUser
from django.contrib.auth.hashers import make_password

class course_form(forms.ModelForm):
    class Meta:
        model=course
        fields=['Image', 'Title', 'Description', 'Tutor', 'Topics', 'Price']

class RegisterForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields =['username','first_name','last_name','email','phone','address','password','picture']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data['password'])
        user.save()  
        return user
    
class ProfileForm(forms.Form):
    username=forms.CharField(max_length=20)
    first_name=forms.CharField(max_length=20)
    last_name=forms.CharField(max_length=20)
    email=forms.EmailField()
    phone=forms.CharField(max_length=15)
    address=forms.CharField(max_length=100)
    

    

class LoginForm(forms.Form):
      username=forms.CharField(max_length=50)
      password=forms.CharField(max_length=50,widget=forms.PasswordInput())

class UserProfileForm(forms.ModelForm):
    class Meta:
        model=CustomUser
        fields="__all__"

        def save(self):
            s=super().save(commit=False)
            s.password=make_password(self.cleaned_data['password'])
            s.save()
            return s
    