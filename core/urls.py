from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('sign-up', views.registration, name = 'signup'),
    path('log-in', views.login_form, name = 'login'),
    path('logout', views.log_out, name = 'logout'),
    path('profile/', views.user_profile, name = 'profile'),
    path('Features/', views.features, name = 'features'),
    path('changeUserPassword', views.changeUserPassword, name = 'changeuserpassword'),
    path('forgotpassword/',views.forgot_password, name="forgotpassword"),
    path('reset_password/<uidb64>/<token>/', views.reset_password, name='resetpassword'),
    path('password_reset_done/', views.password_send_link, name='passwordsendlink'),
    path('productCards/<str:product_category>/', views.productCard, name = 'productcard'),
    path('productDetail/<int:id>/', views.productDetail, name='productdetail'),
    path('sameBrand/<str:brand>/<int:id>/', views.sameBrand, name='samebrand'),
    path('userModelCart/<int:id>/', views.modelSaveCart, name='modelCart'),
    path('addCart/', views.addCart, name='addcart'),
    path('deleteCart/<int:id>/', views.deleteCart, name='deleteCart'),
    path('increaseQuantity/<int:id>/', views.increaseQuantity, name='increasequantity'),
    path('decreaseQuantity/<int:id>/', views.decreaseQuantity, name='decreasequantity'),
    path('userAddress', views.userAddress, name = 'useraddress'),
    path('addUserAddress', views.addUserAddress, name = 'adduseraddress'),
    path('removeUserAddress/<int:id>', views.removeUserAddress, name = 'removeuseraddress'),
    path('editUserAddress/<int:id>', views.editUserAddress, name = 'edituseraddress'),
    path('userCheckout',views.userCheckout, name="usercheckout"),
    path('userPayment', views.userPayment, name='userpayment'),
    path('userPaymentSuccess<int:address>',views.userPaymentSuccess,name='userpaymentsuccess'),
    path('userPaymentFailed',views.userPaymentFailed,name='userpaymentfailed'),
    path('userOrder',views.userOrder,name='userorder'),
    path('userOrderDetails/<int:id>/',views.userOrderDetails,name='userorderdetails'),
    path('userBuyNow/<int:id>/<int:id1>/',views.userBuyNow, name = "userbuynow"),
    path('userPaymentBuyNow/<int:id>/',views.userPaymentBuyNow, name = "userpaymentbuynow"),
    path('userBuyNowPaymentSuccess/<int:addressId>/<int:id>/',views.userBuyNowPaymentSuccess, name = "userbuynowpaymentsuccess"),
    path('userPcBuiltAMD', views.userPcBuiltAMD, name='userpcbuiltamd'),
    path('customDelete/<int:id>', views.deleteBuild, name='buildDelete'),
    path('UsercustomPcheckout/<int:id>/', views.customPcheckout, name='custompcheckout'),
    path('Search', views.search, name='search'),
    path('customPcheckoutPayment', views.customPcheckoutPayment, name='custompcheckoutpayment'),
    path('userCustomPaymentSuccess/<int:address>/', views.userCustomPaymentSuccess, name='usercustompaymentsuccess'),
    path('userCustomPaymentFailed', views.userCustomPaymentFailed, name='usercustompaymentfailed'),
    path('UserBuiltOrder', views.UserBuiltOrder, name='userbuiltorder'),
    path('UserBuildOrderDetail/<int:id>/', views.UserBuildOrderDetail, name='userbuildorderdetail'),
    path('listBuildData/<int:id>/', views.listBuildData, name='listbuilddata'),
    path('aboutSite', views.aboutSite, name='aboutsite'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)