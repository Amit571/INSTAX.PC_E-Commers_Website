from django.contrib import admin
from .models import Category_Card,Product,ModelCart,UserAddress,UserOrder,Carousal,Months_Spacial,CustomPCBuild,CustomBuiltOrder,Profile
# Register your models here.

@admin.register(Category_Card)
class Category_Card_Admin(admin.ModelAdmin):
    list_display = ['card_image', 'card_title', 'link']

admin.site.register(Carousal)
admin.site.register(Product)
admin.site.register(ModelCart)
admin.site.register(UserAddress)
admin.site.register(UserOrder)
admin.site.register(Months_Spacial)
admin.site.register(CustomPCBuild)
admin.site.register(CustomBuiltOrder)
admin.site.register(Profile)