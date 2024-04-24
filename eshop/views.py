from django.shortcuts import render,HttpResponse,redirect
from .models import *
from django.contrib.auth.hashers import check_password,make_password

def index(request):
    # task: create cart or add+/remove- products
    if request.method == 'POST':
        pro_id = request.POST.get('product_id')
        print("product id ----->",pro_id)
        rmv = request.POST.get('remove')
        print('\nremove -----> ',rmv)
        cart_id= request.session.get('cart')
        print("\ncart status ----->",cart_id)
        if cart_id:
            quantity = cart_id.get(pro_id)
            if quantity:
                if rmv:
                    if quantity ==1:
                        cart_id.pop(pro_id)
                    else:
                        cart_id[pro_id] = quantity - 1
                else:
                    cart_id[pro_id] = quantity + 1
            else:
                cart_id[pro_id]=1
        else:
            cart_id = {}
            cart_id[pro_id]=1
        request.session['cart']=cart_id    
        print("3----",request.session['cart'])

    categ_id =  request.GET.get('category_id')
    search = request.GET.get('sch')
    category_obj = Category.objects.all()
    if categ_id:
        product_obj = Product.objects.filter(product_category=categ_id)

    elif search:
        product_obj = Product.objects.filter(product_name__icontains = search)
        
    else:
        product_obj = Product.objects.all()        
    context = {

        'category':category_obj,

        'product':product_obj,

    }

    return render(request,'home.html',context = context)

    

'''(base.html)--->(views.py)--->(models.py)........then redirected to home'''
def registrationform(request):          #function for SIGN-UP / REGISTRATION
    if request.method == 'POST':
        f_name = request.POST.get('fname')  
        l_name = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('pwd')
        mobile = request.POST.get('mbl')
        gender = request.POST.get('gender')
       #data is OBJECT of CLASS Registration......from .models import* that's why
        data = Registration(
            first_name = f_name,
            last_name = l_name,
            email = email,
            password = make_password(password),
            mobile = mobile,
            gender = gender,
        )
        data.save()
    
    return redirect('home')

# case 1: email not found | case 2: email found,wrong password |case 3: email found & correct password
# POST.get('email')<---base.html , user input
# 'email'(Field from models.py, Regi..n)-->(..)POST.get(email=email_id)<--'email_id' is variable(views.py) 


def login(request):
    #email and password we entered
    if request.method == 'POST':
        email_id = request.POST.get('email');
        pass_word = request.POST.get('pwd');
# we have used 'get' NOT 'filter'.......and exception handling
# T R Y   ---   E X C E P T.......otherwise get() gives error instead of "email not found message"
# reques.session[]-----> session is a Dictionary----->(session: railway type/session : FB TYPE)       
        try:
            email_obj = Registration.objects.get(email = email_id)
            if check_password(pass_word,email_obj.password):
                request.session['name'] = email_obj.first_name
                request.session['customer_id'] = email_obj.id
                return redirect('home')
            else:
                return HttpResponse("Wrong Password")
        except:
            return HttpResponse("Email not found")
        
# function to logout
def logout(request):
    request.session.clear()
    return redirect('home')

# function for "C A R T" page
def cartdetails(request):
    if request.session.get('cart',False):
        keys = list(request.session.get('cart').keys())
        p_in_cart = Product.objects.filter(id__in=keys)
        context = {

            'product_in_cart': p_in_cart,

        }
        return render(request, 'cart.html',context=context)
    else:
        return render(request,'cart.html')
        
# function for "O R D E R" page
def checkout_details(request):
    if request.method == 'POST':
        adr = request.POST.get('address')
        mobl = request.POST.get('mobile')
        cid = request.session.get('customer_id')
        cart_id = request.session.get('cart')
        if not cid:
            return HttpResponse('Please Login !')
        product = Product.objects.filter(id__in=list(cart_id.keys()))
        for item in product:
            order_obj = Order(

                address = adr,
                mobile = mobl,
                product = item,
                customer = Registration(id= cid),
                price = item.product_price,
                quantity = cart_id.get(str(item.id)),
            )
            order_obj.save()

    request.session.cart = {}
    return render(request,'order.html')
    
# function RENDERING ----> 'order.html' page
def order_detail(request):
    cust_id = request.session.get('customer_id')
    
    fetch_orders = Order.objects.filter(customer=cust_id)
    tp = 0
    for i in fetch_orders:
        tp = tp + (i.price * i.quantity)
    context = {

        'fetch_orders': fetch_orders,
        'tp':tp,
    }

    return render(request, 'order.html', context = context)

from rest_framework import  viewsets
from .serializers import *

class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
