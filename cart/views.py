from django.shortcuts import render, get_object_or_404
from .cart import Cart
from myapp.models import Product
from django.http import JsonResponse
from django.contrib import messages


def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total()
    return render(request, "cart/cart_summary.html", {"cart_products": cart_products, "quantities": quantities, "totals": totals})


def cart_add(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        # Get product ID from POST
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        # Look up product in DB
        product = get_object_or_404(Product, id=product_id)

        # Add product to cart
        cart.add(product=product, quantity=product_qty)

        cart_quantity = cart.__len__()  # this is okay if your Cart class uses __len__()

        # Prepare response data
        response = JsonResponse({'qty': cart_quantity})
        messages.success(request, "Product added to cart! It’s like a VIP ticket to your shopping spree! 🎟️💸")


        return response


def cart_delete(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        # Get product ID from POST
        product_id = int(request.POST.get('product_id'))

        # Remove the product from the cart
        cart.delete(product=product_id)

        

        # Prepare response
        response = JsonResponse({'product': product_id})
        messages.success(request, "Product deleted successfully! It’s gone like my will to go to the gym! 💨")


        return response



def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # Get product ID from POST
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        cart.update(product=product_id, quantity=product_qty)

        response = JsonResponse({'qty': product_qty})
        messages.success(request, "Product updated! It’s now shining brighter than my dreams after a nap! 🌟💤")


        return response
