from django.shortcuts import render
from store.models import *
import json
from django.http import JsonResponse
import datetime

def cartCookie(request):
    order = {}
    shipping = False
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    print(cart)
    get_cart_items = 0
    get_cart_total = 0
    items = []
    for i in cart:
        get_cart_items += cart[i]['quantity']
        get_cart_total += Product.objects.get(id=i).price * cart[i]['quantity']
        product = Product.objects.get(id=i)
        item = {
            'product': {
                'id': i,
                'name': product.name,
                'price': product.price,
                'imageURL': product.imageURL,
            },
            'quantity': cart[i]['quantity'],
            'Digital': False,
            'get_total': Product.objects.get(id=i).price * cart[i]['quantity']
        }
        items.append(item)
        if product.digital == False:
            shipping = True

    print(items)
    order = {'get_cart_total': get_cart_total, 'get_cart_items': get_cart_items, 'shipping': shipping}
    print(order)
    return {'items': items, 'order': order}