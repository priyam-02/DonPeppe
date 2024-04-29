import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone




class City(models.Model):
    name=models.CharField(max_length=100)
    pin=models.IntegerField()

    class Meta:
        db_table = 'City'

class Register(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    contact=models.CharField(max_length=10)
    address=models.CharField(max_length=800)
    password=models.CharField(max_length=8)
    c_password=models.CharField(max_length=10)
    otp = models.CharField(max_length=10, null=True)
    otp_used = models.IntegerField(null=True)
    city_id=models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id,self.name)

    class Meta:
        db_table='Register'

class Cat(models.Model):
    name=models.CharField(max_length=50)
    def __str__(self):
        return self.name
class sub(models.Model):
        name = models.CharField(max_length=50)
        cat=models.ForeignKey(Cat,on_delete=models.CASCADE)
        def __str__(self):
            return self.name



class Cart(models.Model):
    customer = models.ForeignKey(Register, on_delete=models.CASCADE)
    productd=models.ForeignKey("adminapp.Product", on_delete=models.CASCADE)
    cart_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    completed = models.BooleanField(default=False)

    @property
    def get_cart_total(self):
        cartitems = self.Orderitem_set.all()
        total = sum([item.get_total for item in cartitems])
        return total

    @property
    def get_itemtotal(self):
        cartitems = self.Orderitem_set.all()
        total = sum([item.quantity for item in cartitems])
        return total

    def __str__(self):
        return str(self.id)



class Orderitem(models.Model):

    customer = models.ForeignKey(Register, on_delete=models.CASCADE)
    productd = models.ForeignKey("adminapp.Product", on_delete=models.CASCADE)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price=models.IntegerField()
    total=models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} of {self.productd.proname}"

    def get_total_item_price(self):
        return round(int(self.price) * int(self.quantity))

    def save(self, *args, **kwargs):
        self.total = self.get_total_item_price()
        super().save(*args, **kwargs)


class Order_details(models.Model):

    customer = models.ForeignKey(Register, on_delete=models.CASCADE)

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    oder=models.ManyToManyField(Orderitem,related_name='oder')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    contact = models.CharField(max_length=10)
    address = models.TextField(null=False)
    city_id=models.CharField(max_length=30)
    # pin=models.IntegerField()
    price=models.IntegerField()
    payment=models.CharField(max_length=150,null=False)
    ordered_date = models.DateTimeField(auto_now_add=True)
    payment_id=models.CharField(max_length=500,null=True)
    # item=models.ManyToManyField(Product)
    orderstatus=(
        ('pending','pending'),
        ('Out for shipping', 'Out for shipping'),
        ('completed', 'completed'),

    )

    status=models.CharField(max_length=150,choices=orderstatus,default='pending')
    message=models.TextField(null=True)
    tracking_no=models.CharField(max_length=170,null=True)
    updated_at=models.DateTimeField(auto_now=True)

    # created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return '{} - {}'.format(self.id,self.tracking_no)

class Orderstore(models.Model):

      order=models.ManyToManyField(Order_details,related_name='order')
      price=models.IntegerField()
      customer = models.ForeignKey(Register, on_delete=models.CASCADE)
      datetime_of_payment = models.DateTimeField(default=timezone.now, null=True)

      def __str__(self):
          return '{} - {}'.format(self.order.id, self.order.tracking_no)

class booktable(models.Model):

    customer = models.ForeignKey(Register, on_delete=models.CASCADE)
    person=models.CharField(max_length=40)
    date=models.CharField(max_length=100)
    time=models.CharField(max_length=100)
# Create your models here.
