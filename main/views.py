from django.shortcuts import render, reverse
from .models import NewBalance, Images,Order,OrderItem
from django.http import HttpResponseRedirect
import uuid 
from django.contrib.auth.decorators import login_required 
from services.main import order_data_sender_to_email


def main(req):
    nike = NewBalance.objects.all()
    context  = {'Nike':nike}
    return render(req, 'index.html', context)


def detail(req, id):
    product = NewBalance.objects.get(id=id)
    image = Images.objects.filter(sneakers=product)
    context = {'product':product, 'image':image}
    return render(req, 'detail.html', context)


def favorites(req, id):
    favorite_products = req.session.get('favorite_products', [])
    favorite_products.append(id)
    st = set(favorite_products)
    req.session['favorite_products'] = list(st)
    nike = NewBalance.objects.all()
    context = {'Nike':nike}
    print(st)
    return render(req, 'index.html', context)

def favorites_page(req):
    favorite_product = req.session.get('favorite_products', [])
    favorite_products = NewBalance.objects.filter(id__in = favorite_product)
    context = {'product':favorite_products}
    return render(req, 'favpage.html', context)

def remove_from_favpage(req,id):
    favorite_products = req.session.get('favorite_products', [])
    favorite_products.remove(id)
    req.session['favorite_products'] = favorite_products
    return HttpResponseRedirect('/')

@login_required(login_url='/sign_up/') 
def cart(req, id):
    cart_products = req.session.get('cart_products', [])
    cart_products.append(id)
    st = set(cart_products)
    req.session['cart_products'] = list(st)
    nike = NewBalance.objects.all()
    context = {'Nike':nike}
    print(st)
    return render(req, 'index.html', context)

@login_required(login_url='/sign_up/') 
def cart_page(req):
    cart_product = req.session.get('cart_products', [])
    cart_products = NewBalance.objects.filter(id__in = cart_product)
    total_prise = 0
    for i in cart_products:
        total_prise += i.price
    context = {'product':cart_products, 'amount':cart_products.count(),'total_prise':total_prise}
    return render(req, 'cart.html', context)

@login_required(login_url='/sign_up/') 
def remove_from_cartpage(req,id):
    cart_products = req.session.get('cart_products', [])
    cart_products.remove(id)
    req.session['cart_products'] = cart_products
    return HttpResponseRedirect('/')

def about_us(req):
    info = req.session.get('info', [])
    context = {'info':info}
    return render(req, 'aboutus.html', context)



@login_required(login_url='/sign_up/') 
def order(reqest):
    if reqest.method == 'POST':
        cart_product = reqest.session.get('cart_products', [])
        cart_products = NewBalance.objects.filter(id__in = cart_product)
        total_prise = 0
        for i in cart_products:
            total_prise += i.price
        order = Order.objects.create(
        user = reqest.user, 
        total_prise = total_prise,
        address = reqest.POST.get('address'), 
        code = uuid.uuid4(),  
        phone_number = reqest.POST.get('phone_number'),   
        message = reqest.POST.get('message'),   
        )
        products = []
        for i in cart_products:
            item = OrderItem.objects.create(
                order = order,
                product = i            
            )
            products.append(i)

        order_data_sender_to_email(reqest.user, reqest.POST.get('address'), reqest.POST.get('phone_number'), reqest.POST.get('message'), products)
        cart_products = reqest.session.get('cart_products', [])
        cart_products = []
        reqest.session['cart_products'] = cart_products    
        
    return render(reqest,'order.html')



