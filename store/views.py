from django.shortcuts import render
from .models import *
import json
from django.http import JsonResponse
import datetime
from store.utils import cartCookie

# Create your views here.

def store(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, create = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        content = cartCookie(request)
        order = content['order']
        print('content', content)
        cartItems = order['get_cart_items']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, create = Order.objects.get_or_create(customer = customer, complete=False)
        items = order.orderitem_set.all()
        print(items)
        cartItems = order.get_cart_items
    else:
        content = cartCookie(request)
        items = content['items']
        order = content['order']
        cartItems = order['get_cart_items']
    context = {'items' : items, 'order' : order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, create = Order.objects.get_or_create(customer = customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        content = cartCookie(request)
        items = content['items']
        order = content['order']
        cartItems = order['get_cart_items']

    context = {'items' : items, 'order' : order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer = customer, complete = False)
    orderItem, created = OrderItem.objects.get_or_create(product=product, order=order)

    if(action == 'add'):
        orderItem.quantity += 1
    elif(action == 'remove'):
        orderItem.quantity -= 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    print("Action: ",action)
    print("Product ID: ", productId)


    return JsonResponse("Item added", safe=False)

def processOrder(request):
    data = json.loads(request.body)
    transaction_id = datetime.datetime.now().timestamp()
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['userFormData']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.shipping is not False:
            address = data['shippingInfo']['address']
            city = data['shippingInfo']['city']
            state = data['shippingInfo']['state']
            zipcode = data['shippingInfo']['zipcode']

            shippingAddress, created = ShippingAddress.objects.get_or_create(customer=customer, order=order,
                                                                             address=address,
                                                                             city=city, state=state, zipcode=zipcode)
            shippingAddress.save()

        else:
            print('User not logged in.')

    return JsonResponse("Order proccessed.", safe=False)