from django.db import models

import clientapp.models
from django.core import validators


class Signup(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, validators=[validators.EmailValidator(message="Invalid Email")])
    contact = models.CharField(max_length=10)
    address = models.CharField(max_length=800)
    password = models.CharField(max_length=8)
    c_password = models.CharField(max_length=10)
    otp = models.CharField(max_length=10, null=True)
    otp_used = models.IntegerField(null=True)
    city_id = models.ForeignKey(clientapp.models.City, on_delete=models.CASCADE, null=True)
    img = models.FileField(upload_to='assets/images/products/', default='userd.png')

    def __str__(self):
        return str(self.id, self.name)

    class Meta:
        db_table = 'Adminsignup'


class Cat(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class sub(models.Model):
    name = models.CharField(max_length=50)
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Product(models.Model):
    # customer = models.ForeignKey(Register, on_delete=models.CASCADE, null=True)
    proname=models.CharField(max_length=100)
    prod=models.CharField(max_length=800)
    pimg=models.FileField()
    price=models.IntegerField()
    Category_id = models.ForeignKey(Cat, on_delete=models.SET_NULL,null=True)
    sub_id= models.ForeignKey(sub, on_delete=models.SET_NULL,null=True)
    def __str__(self):
        return '{} - {}'.format(self.id,self.proname)
    class Meta:
        db_table = 'Product'
# Create your models here.
