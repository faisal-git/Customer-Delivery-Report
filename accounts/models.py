from django.db import models

# Create your models here.
class Customer(models.Model):
    name=models.CharField(max_length=200,null=True)
    email=models.EmailField(max_length=50,null=True)
    phone=models.CharField(max_length=20,null=True)
    date_created=models.DateField(auto_now_add=True,null=True)


    def __str__(self):
        return self.name

class Tag(models.Model):
    name=models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.name  

class Product(models.Model):
    CATEGORY=(('Indoor','Indoor'),\
        ('Outdoor','Outdoor'))
    name=models.CharField(max_length=200,null=True)
    price=models.FloatField(max_length=200,null=True)
    category=models.CharField(max_length=200,null=True,choices=CATEGORY)
    description=models.CharField(max_length=500,null=True,blank=True)
    date_created=models.DateField(auto_now_add=True,null=True)
    tag=models.ManyToManyField(Tag)

    def __str__(self):
        return self.name
        

class Order(models.Model):
    customer=models.ForeignKey(Customer,null=True,on_delete=models.SET_NULL)
    product=models.ForeignKey(Product,null=True,on_delete=models.SET_NULL)
    STATUS=(('Pending','Pending'),\
        ('Out for Delivery','Out for Delivery'),\
        ('Delivered','Delivered')
        )
    date_created=models.DateField(auto_now_add=True,null=True)
    status=models.CharField(max_length=20,default='Pending',choices=STATUS)

    def __str__(self):
        return self.customer.name + "\'s order of " +self.product.name
