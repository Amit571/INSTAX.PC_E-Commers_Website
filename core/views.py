from django.http import HttpResponseNotFound
from django.shortcuts import render,HttpResponseRedirect,redirect
from .forms import Registration,UserDataChange,AddressForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from .models import Category_Card,Product,ModelCart,UserAddress,UserOrder,Carousal,Months_Spacial,CustomPCBuild,CustomBuiltOrder,Profile
from django.contrib import messages
from django.shortcuts import get_object_or_404
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from django.urls import reverse
from django.core.mail import send_mail
from django.db.models import Q
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.http import HttpResponse

# defining a function for index.html
# in function we send the data in from Model.
def index(request):
    view_category = Category_Card.objects.all() # Gating all data from CategoryCard Model and store as Object in variable of view_category.
    carousal_data = Carousal.objects.all()[::-1]
    monthSpacialData = Months_Spacial.objects.all()
    productWeekData = Product.objects.filter(deal_category='WEK')[:6]
    topGraphicsCard = Product.objects.filter(category = 'Graphics Card')[:6]
    topProcessors = Product.objects.filter(category = 'Processor')[:6]
    topSSD = Product.objects.all()[:6]

    test = "Hello"
    return render(request, 'core/index.html', {'category' : view_category, 
                                               'carousal_data' : carousal_data, 
                                               'monthData' : monthSpacialData,
                                                'test' : test,
                                                'DataWeek' : productWeekData,
                                                'gpcData' : topGraphicsCard,
                                                'proData' : topProcessors,
                                                'ssdData' : topSSD, }) 

def search(request):
    if request.method == 'POST':
        searchValue = request.POST.get('searchValue')
        if searchValue:
            searchData = Product.objects.filter(Q(productName__icontains=searchValue) | Q(category__icontains=searchValue))
            context = {
                'searchValue': searchValue,
                'searchData': searchData,
            }
            return render(request, 'core/Search.html', context)
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))  # Redirect to the current page or home page if referrer is not available
    return redirect('/')

def send_registration_email(user_email, user_name):
    subject = "Welcome to InstaX – Your Registration is Complete!"
    message = f"""
    Dear {user_name},

    Welcome to InstaX! 🎉

    Your registration is successfully completed, and you’re now part of the InstaX community.
    We’re excited to help you find the perfect PC that suits your needs.

    🚀 What’s Next?  
    ✅ Browse the latest PCs and accessories.  
    ✅ Save your favorite products to your cart.  
    ✅ Enjoy exclusive discounts and offers.  

    🛒 Start Shopping Now:[http://127.0.0.1:8000/]  

    If you didn’t register on InstaX, please ignore this email or contact our support team.  

    📩Need Help? 
    Reach out to us at support@instax.com

    Happy Shopping!  
    The InstaX Team
    """
    send_mail(
        subject,
        message,
        'instax.pc.hub@gmail.com',  # Sender email
        [user_email],  # Recipient email
        fail_silently=False,
    )

# defining a function for User Registration 
# Form.
def registration(request):
    if not request.user.is_authenticated: # If user is not register then:
       
        if request.method == 'POST': # if User is Hit the submit then:
            reg_form = Registration(request.POST) # Access data in Registration Form.

            name = request.POST.get('first_name')
            email = request.POST.get('email')
            
            if reg_form.is_valid(): # check enter data is valid or not.
                reg_form.save() #save Registration Form.

                send_registration_email(email,name)

                return redirect('login') # going to login page.
        else: # incase method is not post.
            reg_form = Registration() # return empty form.

        return render (request, 'core/register.html', {'reg_form':reg_form} ) #form ko render kar registration.html file ko.
    else: # agr user login he to:
        return HttpResponseRedirect('/') # index.html page pe leke ja.



# defining Login form :
def login_form(request):
    if not request.user.is_authenticated: # if user are not login then:
        
        if request.method == 'POST': # agr user ne form submit kiya to:
            login_form = AuthenticationForm(request=request, data = request.POST) # access data in Authentication form:
            login_form.is_valid() # check data is valid or not.
            username = login_form.cleaned_data['username'] # clean data.
            password = login_form.cleaned_data['password'] # clean data.
            user = authenticate(username = username, password = password) # store the data in username and password filed and check its true or not.

            if user is not None: # age data empty nahi he to :
                login(request,user) # request ka data lekar login kar.
                return HttpResponseRedirect('/') # after log in index.html page pe leke ja.
            
        else: # agr method post nahi he to :
            login_form = AuthenticationForm() # empty form return kar.
        return render(request, 'core/login.html', {'login' : login_form}) # render kar login ke sath.
    
    else: # agr authenticate he to:
       return render('/') # index.html page pe leke ja.

# defining a logout function:
def log_out(request):
    logout(request) # auth module ke logout function ko request kar
    return redirect('/') # then index.html ko leke ja.

# profile page ka function.
@login_required
def user_profile(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    if request.method == 'POST':
        form = UserDataChange(request.POST, request.FILES, instance=user, profile_instance=profile)
        if form.is_valid():
            form.save()
            form = UserDataChange(instance=user, profile_instance=profile)
    else:
        form = UserDataChange(instance=user, profile_instance=profile)

    return render(request, 'core/UserProfile.html', {'userData': user, 'form': form})



@login_required
def changeUserPassword(request):
    userData = request.user

    if request.method == 'POST': # agr form submit hogya to.
        changepass = PasswordChangeForm(data = request.POST ,user = request.user) # password change karneka form import keya he. usem user ka data or konsa user login he ye bataya he.
        
        if changepass.is_valid(): # password ka data barabar he to.
            changepass.save() # password change karke save kar.
            update_session_auth_hash(request, changepass.user)  # Ye function password change hone ke bad logout nahi hone keleye.
            
            return redirect('profile') # sab hone ke bad profile pe leja.
        
    else: #agr form subbmit nahi hota to.
        changepass = PasswordChangeForm(user = request.user) # user ko empty form dekha.
    return render(request, 'core/ChangePassword.html', {'userData' : userData,'changepass' : changepass})


def forgot_password(request):  
    if request.method == 'POST':
        email = request.POST['email']
        user = User.objects.filter(email=email).first()
        if user:
            token = default_token_generator.make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = request.build_absolute_uri(f'/reset_password/{uidb64}/{token}/')           
            send_mail(
                'Password Reset',
                f'Click the following link to reset your password: {reset_url}',
                'amitshinde44020t@gmail.com', 
                [email],
                fail_silently=False,
            )
            return redirect('passwordsendlink')
        else:
            messages.success(request,'please enter valid email address')
    return render(request, 'core/forgot_password.html')
                                         

def reset_password(request, uidb64, token):
    if request.method == 'POST':
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            try:
                uid = force_str(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk=uid)
                if default_token_generator.check_token(user, token):
                    user.set_password(password)
                    user.save()
                    return redirect('login')
                else:
                    return HttpResponse('Token is invalid', status=400)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                return HttpResponse('Invalid link', status=400)
        else:
            return HttpResponse('Passwords do not match', status=400)
    return render(request, 'core/reset_password.html')

def password_send_link(request):
    return render(request, 'core/password_link_send.html')


def features(request):
    return render(request, 'core/Features.html')

def aboutSite(request):
    return render(request, 'core/AboutUs.html')


# Product Function
def productCard(request,product_category):
    productCardsData = Product.objects.filter(category = product_category)
    return render(request, 'core/ProductCards.html', {'pggd':productCardsData, 'categoryname' : product_category})

def productDetail(request, id):
    product = Product.objects.get(pk=id)  # Fetch product by ID
    return render(request, 'core/productdetails.html', {'product':product})

def sameBrand(request, brand, id):
    products = Product.objects.filter(brand__iexact=brand).exclude(id=id)  # Filter products by brand (case-insensitive) and exclude the specified product ID
    return render(request, 'core/SameBrand.html', {'products': products, 'brand': brand})


@login_required(login_url='login')  # Redirect to login page if not logged in
def modelSaveCart(request, id):
    user = request.user
    product = Product.objects.get(pk=id)

    ModelCart(user=user, product=product).save()
    messages.success(request, 'Added to cart successfully!')

    return redirect('productdetail', id)


@login_required
def get_cart_details(request):
    add = ModelCart.objects.filter(user=request.user)
    address = UserAddress.objects.filter(user = request.user)
    count = add.count()
    total = sum(item.price_and_quantity_total for item in add)

    charges = 0
    package = 49
    delivery = "FREE"
    
    # Apply 20% discount
    discount = min(int(total * 0.20), total)

    # Calculate delivery charges
    if total == 0:
        charges = 0
        package = 0
        delivery = 0
    elif total < 500:
        delivery = 49
        charges = 49

    packageCharge = 0 if package == 0 else 49

    # Final total calculation
    finalTotal = (total - discount) + charges + package

    return {
        'add': add,
        'count': count,
        'total': total,
        'discount': discount,
        'delivery': delivery,
        'packageCharge': packageCharge,
        'finalTotal': finalTotal,
        'address' : address
    }

@login_required
def addCart(request):
    context = get_cart_details(request)
    return render(request, 'core/UserCart.html',context)

@login_required
def increaseQuantity(request,id):
    product = get_object_or_404(ModelCart,pk=id)
    product.quantity+=1
    product.save()
    return redirect('addcart')

@login_required
def decreaseQuantity(request,id):

    product = get_object_or_404(ModelCart,pk=id)
    price = get_object_or_404(ModelCart,pk=id)
    product.quantity-=1
    product.save()

    if product.quantity == 0:
        dele = ModelCart.objects.get(pk=id)
        dele.delete()
    return redirect('addcart')


@login_required
def deleteCart(request ,id):
    dele = ModelCart.objects.get(pk=id)
    dele.delete()
    return redirect('addcart')

# Custom PC Built
@login_required(login_url='login')
def userPcBuiltAMD(request):
    total_price = None  # Initialize it with None or 0

    if request.method == 'POST':
        # Get all selected product instances
        motherboard = get_object_or_404(Product, id=request.POST.get('motherboard_id'))
        processor = get_object_or_404(Product, id=request.POST.get('processor_id'))
        ram = get_object_or_404(Product, id=request.POST.get('ram_id'))
        hdd = get_object_or_404(Product, id=request.POST.get('hdd_id'))
        ssd = get_object_or_404(Product, id=request.POST.get('ssd_id'))
        power_supply = get_object_or_404(Product, id=request.POST.get('power_id'))
        graphics_card = get_object_or_404(Product, id=request.POST.get('graphics_id'))
        cooler = get_object_or_404(Product, id=request.POST.get('cooler_id'))
        cabinet = get_object_or_404(Product, id=request.POST.get('cabinet_id'))

        # Calculate total price
        total_price = (
            motherboard.price +
            processor.price +
            ram.price +
            hdd.price +
            ssd.price +
            power_supply.price +
            graphics_card.price +
            cooler.price +
            cabinet.price
        )

        discount = min(int(total_price * 0.20), total_price)
        charges = 0
        if total_price > 500:
            delivery = 'FREE'
        else :
            charges = 50

        packageCharge = 549

        finalTotal = (total_price - discount) + charges + packageCharge

        # Delete previous builds
        # CustomPCBuild.objects.filter(user=request.user).delete()

        # Create new build
        CustomPCBuild.objects.create(
            user=request.user,
            motherboard=motherboard,
            processor=processor,
            ram=ram,    
            hdd=hdd,
            ssd=ssd,
            power_supply=power_supply,
            graphics_card=graphics_card,
            cooler=cooler,
            cabinet = cabinet,
            total_price= finalTotal 
        )

        #Making a count of product
        custom_build = CustomPCBuild.objects.filter(user=request.user).first()

        if not custom_build:
            total_items = 0
        else:
            total_items = 0
            # List all fields you want to check
            components = [
                custom_build.motherboard,
                custom_build.processor,
                custom_build.ram,
                custom_build.hdd,
                custom_build.ssd,
                custom_build.power_supply,
                custom_build.graphics_card,
                custom_build.cooler,
                custom_build.cabinet,
            ]

            # Count non-null items
            total_items = sum(1 for item in components if item is not None)

        request.session['total_price'] = total_price
        request.session['discount'] = discount
        request.session['delivery'] = delivery
        request.session['packageCharge'] = packageCharge
        request.session['finalTotal'] = finalTotal
        request.session['total_items'] = total_items
        return redirect('userpcbuiltamd')

    customPcData = CustomPCBuild.objects.filter(user=request.user)[::-1]

    context = {
        'MbData': Product.objects.filter(category='Motherboard'),
        'ProsData': Product.objects.filter(category='Processor'),
        'RamData': Product.objects.filter(category='Ram'),
        'HddData': Product.objects.filter(category='Hard Disk'),
        'PowerSupplyData': Product.objects.filter(category='Power Supply'),
        'GraphicsCardData': Product.objects.filter(category='Graphics Card'),
        'SsdData': Product.objects.filter(category='Solid State Drive'),
        'CoolersData': Product.objects.filter(Q(category='Air Cooler') | Q(category='Liquid Cooler')),
        'cabinetData': Product.objects.filter(category='Cabinet'),
        'Total': total_price, # total_price will be None during GET
        'customPcData' : customPcData
    }
    return render(request, 'core/UserPcBuilt.html', context)

@login_required
def deleteBuild(request, id):
    dele = CustomPCBuild.objects.get(pk=id)
    dele.delete()
    return redirect('userpcbuiltamd')

@login_required
def customPcheckout(request, id):
    contextData = get_cart_details(request)
    address = contextData['address']

    # Get the specific build by ID
    customPcData = get_object_or_404(CustomPCBuild, pk=id, user=request.user)

    # Use the build's stored values
    total_price = customPcData.total_price
    total_items = sum(1 for item in [
        customPcData.motherboard,
        customPcData.processor,
        customPcData.ram,
        customPcData.hdd,
        customPcData.ssd,
        customPcData.power_supply,
        customPcData.graphics_card,
        customPcData.cooler,
        customPcData.cabinet,
    ] if item)

    discount = min(int(total_price * 0.20), total_price)
    delivery = 'FREE' if total_price > 500 else 'PAID'
    packageCharge = 549
    finalTotal = (total_price - discount) + (0 if delivery == 'FREE' else 50) + packageCharge

    context = {
        'address': address,
        'customPcData': customPcData,
        'total': total_price,
        'discount': discount,
        'delivery': delivery,
        'packageCharge': packageCharge,
        'finalTotal': finalTotal,
        'count': total_items,
    }
    return render(request, 'core/UserCustomPCheckOut.html', context)

@login_required
def listBuildData(request,id):
    data = CustomPCBuild.objects.get(pk=id)
    context = { 'data' : data }
    return render(request, 'core/UserBuildDetailsShow.html', context)


@login_required
def customPcheckoutPayment(request):
    customData = CustomPCBuild.objects.filter(user = request.user).first()
    totalCustomAmount = customData.total_price if customData else 0
    inr_amount = totalCustomAmount
    usd_amount = round(inr_amount / 85.36, 2) 
    if request.method == 'POST':
        address = request.POST.get('address')
    
    if request.method == 'POST' and request.POST.get('address'):
        host = request.get_host()   # Will fecth the domain site is currently hosted on.
        paypal_checkout = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,   #This is typically the email address associated with the PayPal account that will receive the payment.
            'amount': usd_amount,    #: The amount of money to be charged for the transaction. 
            'item_name': 'Product',       # Describes the item being purchased.
            'invoice': uuid.uuid4(),  #A unique identifier for the invoice. It uses uuid.uuid4() to generate a random UUID.
            'currency_code': 'USD',
            'notify_url': f"http://{host}{reverse('paypal-ipn')}",         #The URL where PayPal will send Instant Payment Notifications (IPN) to notify the merchant about payment-related events
            'return_url': f"http://{host}{reverse('usercustompaymentsuccess',args=[address])}",     #The URL where the customer will be redirected after a successful payment. 
            'cancel_url': f"http://{host}{reverse('usercustompaymentfailed')}",      #The URL where the customer will be redirected if they choose to cancel the payment. 
        }

        paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)
    else:
        return redirect('adduseraddress')

    return render(request, 'core/userPaymentWork.html', {'paypal':paypal_payment})

@login_required
def userCustomPaymentSuccess(request, address):
    user = request.user
    addressData = get_object_or_404(UserAddress, pk=address)
    customBuild = CustomPCBuild.objects.filter(user=user).first()

    if customBuild:
        # Save the finalized order
        CustomBuiltOrder.objects.create(
            user=user,
            address=addressData,
            motherboard=customBuild.motherboard,
            processor=customBuild.processor,
            ram=customBuild.ram,
            hdd=customBuild.hdd,
            ssd=customBuild.ssd,
            power_supply=customBuild.power_supply,
            graphics_card=customBuild.graphics_card,
            cooler=customBuild.cooler,
            cabinet=customBuild.cabinet,
            total_price=customBuild.total_price
        )

        # Clean up the build
        customBuild.delete()

    return render(request, 'core/UserPaymentSuccess.html')

@login_required
def userCustomPaymentFailed(request):
    return render(request,'core/UserPaymentFailed.html')

@login_required
def UserBuiltOrder(request):
    userData = request.user
    customOrderData = CustomBuiltOrder.objects.filter(user = request.user)[::-1]
    context = {'customOrderData' : customOrderData,
               'userData' : userData}
    return render (request,'core/UserBuildOrder.html', context)

@login_required
def UserBuildOrderDetail(request, id):
    orderData = get_object_or_404(CustomBuiltOrder,pk=id)
    context = {'orderData' : orderData}
    return render(request, 'core/UserBuildOrderDetail.html', context)
    

@login_required
def userCheckout(request):
    context = get_cart_details(request)
    return render(request,'core/UserCheckout.html', context)

@login_required
def userPayment(request):

    contextData = get_cart_details(request)
    totalAmount = contextData['finalTotal']
    inr_amount = totalAmount
    usd_amount = round(inr_amount / 85.36, 2) 

    if request.method == 'POST':
        address = request.POST.get('address')
        
    if request.method == 'POST' and request.POST.get('address'):
        host = request.get_host()   # Will fecth the domain site is currently hosted on.
        paypal_checkout = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,   #This is typically the email address associated with the PayPal account that will receive the payment.
            'amount': usd_amount,    #: The amount of money to be charged for the transaction. 
            'item_name': 'Product',       # Describes the item being purchased.
            'invoice': uuid.uuid4(),  #A unique identifier for the invoice. It uses uuid.uuid4() to generate a random UUID.
            'currency_code': 'USD',
            'notify_url': f"http://{host}{reverse('paypal-ipn')}",         #The URL where PayPal will send Instant Payment Notifications (IPN) to notify the merchant about payment-related events
            'return_url': f"http://{host}{reverse('userpaymentsuccess',args=[address])}",     #The URL where the customer will be redirected after a successful payment. 
            'cancel_url': f"http://{host}{reverse('userpaymentfailed')}",      #The URL where the customer will be redirected if they choose to cancel the payment. 
        }
    else:
        return redirect('adduseraddress')
    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

    return render(request, 'core/userPaymentWork.html', {'paypal':paypal_payment})

@login_required
def userPaymentSuccess(request,address):
    user= request.user
    addressData = UserAddress.objects.get(pk=address)
    cartData = ModelCart.objects.filter(user=request.user)

    for cart in cartData:
        UserOrder(user=user, address=addressData, quantity=cart.quantity, product=cart.product).save()
        
        cartData.delete()

    return render(request,'core/UserPaymentSuccess.html')

@login_required
def userPaymentFailed(request):
    return render(request,'core/UserPaymentFailed.html')

@login_required
def userOrder(request):
    userData = request.user
    orderData = UserOrder.objects.filter(user = request.user)[::-1]

    return render(request, 'core/UserOrder.html', {'userData' : userData, 'orderData' : orderData })

@login_required
def userOrderDetails(request,id):
    orderData = get_object_or_404(UserOrder,pk=id)
    return render(request, 'core/UserOrderDetails.html', {'orderData' : orderData})

@login_required
def userBuyNow(request, id, id1):
    address = UserAddress.objects.filter(user = request.user)

    productData = get_object_or_404(Product,pk=id)
    cartData = get_object_or_404(ModelCart, pk=id1)

    count = cartData.quantity
    sum = productData.price*cartData.quantity

    charges = 0
    package = 49
    delivery = "FREE"
    
    # Apply 20% discount
    discount = min(int(sum * 0.20), sum)

    # Calculate delivery charges
    if sum == 0:
        charges = 0
        package = 0
        delivery = 0
    elif sum < 500:
        delivery = 49
        charges = 49

    packageCharge = 0 if package == 0 else 49

    # Final total calculation
    finalTotal = (sum - discount) + charges + package

    # Store finalTotal in session
    request.session['finalTotal'] = finalTotal
    return render(request, 'core/UserBuyNow.html', {'address': address, 
                                                    'productData' : productData, 
                                                    'cartData' : cartData , 
                                                    'finalTotal': finalTotal, 
                                                    'count' : count, 'total' : sum, 
                                                    'discount' : discount, 
                                                    'delivery' : delivery, 
                                                    'packageCharge' : packageCharge})

@login_required
def userPaymentBuyNow(request,id):

    finalTotal = request.session.get('finalTotal', 0)
    inr_amount = finalTotal
    usd_amount = round(inr_amount / 85.36, 2) 

    if request.method == 'POST' and request.POST.get('selectedAddress'):
        addressId = request.POST.get('selectedAddress')
        host = request.get_host()   # Will fetch the domain site is currently hosted on.
        paypal_checkout = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': usd_amount,
            'item_name': 'Product',
            'invoice': uuid.uuid4(),
            'currency_code': 'USD',
            'notify_url': f"http://{host}{reverse('paypal-ipn')}",
            'return_url': f"http://{host}{reverse('userbuynowpaymentsuccess', args=[addressId, id])}",
            'cancel_url': f"http://{host}{reverse('userpaymentfailed')}",
        }

        paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)
        return render(request, 'core/userPaymentWork.html', {'paypal': paypal_payment})
    else:
        return redirect('adduseraddress')

@login_required
def userBuyNowPaymentSuccess(request,addressId,id):
   
    user = request.user
    address = UserAddress.objects.get(pk = addressId)
    cartData = ModelCart.objects.get(pk=id)
    quantityData = cartData.quantity
    product = cartData.product

    UserOrder(user = user,
              address = address,
              product =  product,
              quantity = quantityData).save()
    
    cartData.delete()

    return render(request,'core/UserPaymentSuccess.html')

@login_required
def userPaymentBuyNowFailed(request):
    return redirect('userpaymentfailed')

@login_required
def addUserAddress(request):
    userData = request.user  # Get the logged-in user

    if request.method == 'POST':
        formData = AddressForm(request.POST)

        if formData.is_valid():
            address = formData.save(commit=False)  # Create an instance but don't save it yet
            address.user = request.user  # Assign the logged-in user
            address.save()  # Now save it
            return redirect('useraddress')  # Redirect after saving
    else:
        formData = AddressForm()  # Create an empty form for GET request
    return render(request, 'core/AddUserAddress.html', {'userData': userData, 'formData': formData})

@login_required
def userAddress(request):
    userData = request.user
    modelData = UserAddress.objects.filter(user=request.user)  # Fetch user's addresses

    return render(request, 'core/UserAddress.html', {'userData': userData, 'modelData': modelData})

@login_required
def removeUserAddress(request,id):
    modelData = UserAddress.objects.get(pk=id)  # Fetch user's addresses
    modelData.delete()
    return redirect('useraddress')

@login_required
def editUserAddress(request,id):
    userData = request.user

    modelData = UserAddress.objects.get(pk=id)  # Fetch user's addresses
    formData = AddressForm(request.POST or None, instance=modelData)

    if formData.is_valid():
        formData.save()
        return redirect('useraddress')
    return render(request,'core/EditUserAddress.html', {'formData' : formData , 'userData' : userData})