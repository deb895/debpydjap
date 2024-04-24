from django.db import models

# table 1 - Registration
                    #INHERITENCE
class Registration(models.Model):
    first_name = models.CharField(max_length = 100,blank=True,null=True,default='')
    last_name = models.CharField(max_length = 100,blank=True,null=True,default='')
    email = models.CharField(max_length = 100,blank=True,null=True,default='',unique = True)
    password = models.CharField(max_length = 255,blank=True,null=True,default='')
    mobile = models.BigIntegerField(default=0)
    gender = models.CharField(max_length = 100,blank=True,null=True,default='')

    def __str__(self):
        return self.first_name


# table 2 - Category 
class Category(models.Model):
    category_name = models.CharField(max_length=100, blank=True, null=True)
    category_image = models.ImageField(upload_to = "upload/category/")
    def __str__(self):
        return self.category_name    

# table 3 - Product
class Product(models.Model):
    product_name        = models.CharField(max_length=100 ,blank = True, null = True) 
    product_image       = models.ImageField(upload_to="upload/product/")
    product_description = models.CharField(max_length = 200 ,blank = True, null = True)
    product_price       = models.IntegerField()
    product_category    = models.ForeignKey(Category, on_delete = models.CASCADE)

    def __str__(self):
        return self.product_name

# table 4 - Order details
class Order(models.Model):
    address = models.CharField(max_length=200, blank=True)
    mobile = models.BigIntegerField()
    product = models.ForeignKey(Product,on_delete = models.CASCADE)
    customer = models.ForeignKey(Registration,on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity =models.IntegerField() 
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.customer.first_name