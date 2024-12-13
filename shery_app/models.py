from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class course(models.Model):
    Image=models.FileField(upload_to='images/')
    Title=models.CharField(max_length=50)
    Description=models.CharField(max_length=400)
    Tutor=models.CharField(max_length=50)
    Topics=models.JSONField()
    Price=models.IntegerField()

    def __str__(self):
        return self.Title

class CustomUser(AbstractUser):
    picture=models.FileField(upload_to='profile_pictures/',null=True,default=None,blank=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    emailaddress=models.EmailField(default='example@example.com')
    

    def __str__(self):
        return self.username
    
class Cart(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
    def total_price(self):
        total=0
        for i in self.cartitem_set.all():
            total+=i.get_total_price()
        return total
    
class CartItem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    course=models.ForeignKey(course,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.course.Title}x{self.quantity}"
    
    def get_total_price(self):
        return self.course.Price * self.quantity
    
class Enrollement(models.Model):
     user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
     course=models.ForeignKey(course,on_delete=models.CASCADE)

     def __str__(self):
         return f'{self.user.username} <----> {self.course.Title}'
 

    