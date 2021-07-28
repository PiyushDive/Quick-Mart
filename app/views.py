from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerRegistrationForm, ProfileForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.db.models import Q, query

class HomeView(View):
    def get(self, request):
        total_items = 0
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        # laptops = Product.objects.filter(category='L')
        if request.user.is_authenticated:
            total_items = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/home.html',
         {'topwears':topwears,'bottomwears':bottomwears,
          'mobiles':mobiles, 'total_items':total_items})

class ProductDetailView(View):
    def get(self, request, pk):
        total_items = 0
        product = Product.objects.get(pk=pk)
        item_exist_in_cart = False
        if request.user.is_authenticated:
            item_exist_in_cart = Cart.objects.filter(Q(product=product.id)
             & Q(user=request.user)).exists()

            total_items = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/productdetail.html', {'product':product,
         'item_exist_in_cart':item_exist_in_cart, 'total_items':total_items})

def mobile(request, data=None):
    total_items = 0
    if data == None:
        mobiles = Product.objects.filter(category='M')
    
    elif data == 'Redmi' or data == 'Oppo' or data == 'Samsung':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    
    elif data == 'Below':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=10000)
    
    elif data == 'Above':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=10000)
    
    if request.user.is_authenticated:
        total_items = len(Cart.objects.filter(user=request.user))
    
    return render(request, 'app/mobile.html', {'mobiles':mobiles, 'total_items':total_items})

@csrf_exempt
def customerregistration(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  
            user.save()
            messages.success(request, "Congratulations!! Registered Successfully")   
    else:
        form = CustomerRegistrationForm()
    
    return render(request, 'app/customerregistration.html', {'form':form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Successfully Logged Out !')
    return redirect('login')

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            profile = Customer(user=user, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            profile.save()
            messages.success(request, "Profile Updated successfully !!")
            return redirect('address')
    else:
        form = ProfileForm()

    if request.user.is_authenticated:
        total_items = len(Cart.objects.filter(user=request.user))
    
    return render(request, 'app/profile.html', {'form':form, 'total_items':total_items})

@login_required
def address(request):
    addresses = Customer.objects.filter(user=request.user)

    if request.user.is_authenticated:
        total_items = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/address.html', {'addresses':addresses, 'total_items':total_items})

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/show_cart')

@login_required
def show_cart(request): 
    if request.user.is_authenticated:
        total_items = len(Cart.objects.filter(user=request.user))

        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        shipping_amount = 70
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        
        if cart_product:
            for p in cart_product:
                temp_amount = (p.quantity * p.product.discounted_price)
                amount = int(temp_amount) + amount
                total_amount = amount + shipping_amount
            return render(request, 'app/addtocart.html', {'carts':cart, 
             'amount':amount, 'total_amount':total_amount, 'total_items':total_items})
        else:
            return render(request, 'app/empty_cart.html')

@login_required
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        user = request.user
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0
        shipping_amount = 70
        cart_product = [p for p in Cart.objects.all() if p.user == user]

        for p in cart_product:
            temp_amount = (p.quantity * p.product.discounted_price)
            amount = int(temp_amount) + amount        

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'total_amount': amount + shipping_amount
        }
    return JsonResponse(data)

@login_required
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        user = request.user
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        amount = 0
        shipping_amount = 70
        cart_product = [p for p in Cart.objects.all() if p.user == user]

        for p in cart_product:
            temp_amount = (p.quantity * p.product.discounted_price)
            amount = int(temp_amount) + amount     

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'total_amount': amount + shipping_amount
        }
    return JsonResponse(data)

@login_required
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        user = request.user
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0
        shipping_amount = 70
        cart_product = [p for p in Cart.objects.all() if p.user == user]

        for p in cart_product:
            temp_amount = (p.quantity * p.product.discounted_price)
            amount = int(temp_amount) + amount         

        data = {
            'amount': amount,
            'total_amount': amount + shipping_amount
        }
    return JsonResponse(data)

@login_required
def checkout(request):
    user = request.user
    address = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0
    shipping_amount = 70
    cart_product = [p for p in Cart.objects.all() if p.user == user]

    if cart_product:
        for p in cart_product:
            temp_amount = (p.quantity * p.product.discounted_price)
            amount += int(temp_amount)
            total_amount = amount + shipping_amount

    if request.user.is_authenticated:
        total_items = len(Cart.objects.filter(user=request.user))

    return render(request, 'app/checkout.html', {'address':address,
     'cart_items':cart_items, 'total_amount':total_amount,
      'amount':amount, 'total_items':total_items}, )

@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    try:
        customer = Customer.objects.get(id=custid)
    except Customer.DoesNotExist:
        user = None
    cart = Cart.objects.filter(user=user)

    for c in cart:
        OrderPlaced(user=user, customer=customer, 
        product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect('orders')

@login_required
def orders(request):
    user = request.user
    order_items = OrderPlaced.objects.filter(user=user)

    if request.user.is_authenticated:
        total_items = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/orders.html', 
    {'order_items':order_items, 'total_items':total_items})

@login_required
def buy_now(request):
    user = request.user
    prod_id = request.GET.get('p_id')
    product = Product.objects.get(id=prod_id)
    address = Customer.objects.filter(user=user)

    shipping_amount = 70
    amount = product.discounted_price
    total_amount = amount + shipping_amount

    if request.user.is_authenticated:
        total_items = len(Cart.objects.filter(user=request.user))

    return render(request, 'app/buynow.html', 
    {'product':product, 'address':address,
     'total_amount':total_amount, 'total_items':total_items})

# def search(request):
#     query = request.GET.get('query')
#     if len(query) < 30:
        

#     return render(request, 'search.html', {'query':query, })