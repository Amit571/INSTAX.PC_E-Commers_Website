from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField()
    mobile = models.CharField(max_length=10)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    def __str__(self):
        return self.user.username


# Create your models here.
class Carousal(models.Model):
    carousalImages = models.ImageField(upload_to = 'carousal_image', default=1)
    imageName = models.CharField(max_length=20, default='carousal_images')

    def __str__(self):
        return self.imageName

class Category_Card(models.Model):
    CATEGORY_LINKS = [
        ('/personalHealth/', 'Personal Health'),
        ('/smartPhones/', 'Smart Phones'),
        ('/homeAppliances/', 'Home Appliances'),
        ('/gamingGadgets/', 'Gaming Gadgets'),
    ]
    card_image = models.ImageField(upload_to = 'category_images')
    card_title = models.CharField(max_length=50)
    link = models.CharField(max_length=100, choices=CATEGORY_LINKS, default='/electronics/')

    def __str__(self):
        return self.card_title

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('Ram', 'PC RAM'),
        ('Graphics Card', 'GRAPHICS CARDS'),
        ('Air Cooler', 'AIR COOLER'),
        ('Hard Disk', 'HARD DRIVE'),
        ('Power Supply', 'POWER SUPPLY'),
        ('Solid State Drive', 'SSD'),
        ('Liquid Cooler', 'LIQUID COOLER'),
        ('Processor', 'PROCESSOR'),
        ('Motherboard', 'MOTHERBOARD'),
        ('Cabinet', 'CABINET'),
        ('Monitor', 'MONITOR'),
        ('Mouse', 'MOUSE'),
        ('Keyboard', 'KEYBOARD'),
        ('Gaming Accessory', 'GAMING ACCESSORY'),

    ]

    DEAL_CHOICE = [
        ('WEK', 'WEEKLY DEAL'),
        ('SPA', 'SPACIAL DEAL'),
    ]

    TIME_CHOICE = [
        ('15 MINIS', '15 minis'),
        ('30 MINIS', '30 minis'),
        ('01 HUR', '01 hur')
    ]

    PRODUCT_TYPE = [
        ('One Unit', '1 Unit'),
        ('Set', 'Set'),
        ('Combo', 'Combo')
    ]

    productName = models.CharField(max_length=50)
    category = models.CharField(max_length=50, choices= CATEGORY_CHOICES)
    deal_category = models.CharField(max_length=50, choices= DEAL_CHOICE, null=True, blank=True)
    price = models.IntegerField()
    description = models.CharField(max_length=50)
    productImages = models.ImageField(upload_to = 'product_images', blank=True, null=True)
    productImages1 = models.ImageField(upload_to = 'product_images', blank=True, null=True)
    productImages2 = models.ImageField(upload_to = 'product_images', blank=True, null=True)
    productImages3 = models.ImageField(upload_to = 'product_images', blank=True, null=True)
    time = models.CharField(max_length= 20, choices= TIME_CHOICE)
    type = models.CharField(max_length= 20, choices= PRODUCT_TYPE)
    brand = models.CharField(max_length=50, null=True, blank=True)
    point1 = models.CharField(max_length=255, null=True, blank=True)
    point2 = models.CharField(max_length=255, null=True, blank=True)
    point3 = models.CharField(max_length=255, null=True, blank=True)
    point4 = models.CharField(max_length=255, null=True, blank=True)


    def __str__(self):
        return self.productName
    
class ModelCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.product)
    
    @property
    def price_and_quantity_total(self):
        return self.product.price*self.quantity

class UserAddress(models.Model):
    TYPE_COSIES = [('Home','Home'),('Office','Office')]
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    state = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    area = models.CharField(max_length=30)
    block = models.CharField(max_length=20)
    landmark = models.CharField(max_length=40)
    pin = models.CharField(max_length=6)
    addressType = models.CharField(max_length=20, choices=TYPE_COSIES,default='H')
    mobile = models.CharField(max_length=10)
    fullName = models.CharField(max_length=30)

    def __str__(self):
        return self.city

class UserOrder(models.Model):
    STATUS_CHOICES = [
        ('15', '15 minuets'),
        ('12', '12 minuets'),
        ('9', '9 minuets'),
        ('6', '6 minuets'),
        ('3', '3 minuets'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(UserAddress, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='15')

    def __str__(self):
        return str(self.product)
    
class Months_Spacial(models.Model):
    news_tital= models.CharField(max_length=250, null=True, blank=True)
    news_description = models.CharField(max_length=250, null=True, blank=True)
    news_link = models.URLField(max_length=250, null=True, blank=True)
    news_image = models.ImageField(upload_to = 'news_images', null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
 

class CustomPCBuild(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    motherboard = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='motherboard_builds')
    processor = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='processor_builds')
    ram = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='ram_builds')
    hdd = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='hdd_builds')
    ssd = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='ssd_builds')
    power_supply = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='power_builds')
    graphics_card = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='graphics_builds')
    cooler = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='cooler_builds')
    cabinet = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='cabinet_builds')
    total_price = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.username}'s Build - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"


class CustomBuiltOrder(models.Model):
    STATUS_CHOICES = [
        ('15', '3 Hur'),
        ('12', 'Find Product'),
        ('9', 'Assembling'),
        ('6', 'Software'),
        ('3', 'Pack and Outofdelivrary'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey('UserAddress', on_delete=models.CASCADE)
    
    motherboard = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='order_motherboard')
    processor = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='order_processor')
    ram = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='order_ram')
    hdd = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='order_hdd')
    ssd = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='order_ssd')
    power_supply = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='order_power')
    graphics_card = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='order_graphics')
    cooler = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='order_cooler')
    cabinet = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='order_cabinet')

    total_price = models.IntegerField()
    ordered_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='15')

    user_order_id = models.IntegerField()

    def save(self, *args, **kwargs):
        if not self.pk:
            # Get the max user_order_id for this user
            last_order = CustomBuiltOrder.objects.filter(user=self.user).order_by('-user_order_id').first()
            self.user_order_id = 1 if not last_order else last_order.user_order_id + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.user_order_id} - {self.ordered_at.strftime('%Y-%m-%d')}"