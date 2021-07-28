from django.db import models
from django.contrib.auth.models import User
from django.core.validators import  MaxValueValidator, MinValueValidator

STATE_CHOICES = (
    ('Andaman & Nicobar Islands', 'Andaman & Nicobar Islands'),
    ('Arunachal Pradesh', 'Arunachal Pradesh'),
    ('Andhra Pradesh', 'Andhra Pradesh'),
    ('Assam', 'Assam'),
    ('Bihar', 'Bihar'),
    ('Maharashtra', 'Maharashtra'),
    ('Chandigarh', 'Chandigarh'),
    ('Chhattisgarh', 'Chhattisgarh'),
    ('Dadra & Nager Haveli', 'Dadra & Nager Haveli'),
    ('Daman & Diu', 'Daman & Diu'),
    ('Goa', 'Goa'),
    ('Gujrat', 'Gujrat'),
    ('Haryana', 'Haryana'),
    ('Himachal Pradesh', 'Himachal Pradesh'),
    ('Jammu & Kashmir', 'Jammu & Kashmir'),
    ('Jharkhand', 'Jharkhand'),
    ('Karnataka', 'Karnataka'),
    ('Kerela', 'Kerela'),
    ('Lakshadweep', 'Lakshadweep'),
    ('Mahya Pradesh', 'Mahya Pradesh'),
    ('Manipur', 'Manipur'),
    ('Meghalaya', 'Meghalaya'),
    ('Mizoram', 'Mizoram'),
    ('Nagaland', 'Nagaland'),
    ('Odisa', 'Odisa'),
    ('Puducherry', 'Puducherry'),
    ('Punjab', 'Punjab'),
    ('Rajasthan', 'Rajasthan'),
    ('Sikkim', 'Sikkim'),
    ('Tamil Nadu', 'Tamil Nadu'),
    ('Telangana', 'Telangana'),
    ('Tripura', 'Tripura'),
    ('Uttarakhand', 'Uttarakhand'),
    ('Uttar Pradesh', 'Uttar Pradesh'),
    ('West Bengal', 'West Bengal')
)

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    name = models.CharField(max_length = 100)
    locality = models.CharField(max_length = 200)
    city = models.CharField(max_length = 50)
    zipcode = models.IntegerField()
    state = models.CharField(choices = STATE_CHOICES, max_length=50)

    def __str__(self):
        return str(self.id)

CATEGORY_CHOICES = (
    ('M', 'Mobile'),
    ('L', 'Laptop'),
    ('TW', 'Top Wear'),
    ('BW', 'Bottom Wear')
)

class Product(models.Model):
    title = models.CharField(max_length = 100)
    selling_price = models.DecimalField(max_digits=15, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.TextField()
    brand = models.CharField(max_length = 100)
    category = models.CharField(choices = CATEGORY_CHOICES,  max_length = 3)
    product_image = models.ImageField(upload_to='productimg')

    def __str__(self):
        return str(self.id)

    @property
    def save_amount(self):
        return self.selling_price - self.discounted_price
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    product = models.ForeignKey(Product, on_delete= models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def  __str__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price


STATUS_CHOICES=(
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancle', 'Cancle'),
    ('Pending...', 'Pending...'),
)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES, default='Pending...', max_length = 50)

    def  __str__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
