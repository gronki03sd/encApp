from django.shortcuts import render
from cart.cart import Cart




def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    cart_total = cart.cart_total()  # Changed from "totals" to "cart_total" to match template
    
    # You might want to calculate tax and shipping here
    tax = cart_total * 0.1  # Example: 10% tax
    shipping = 5.00  # Example: flat rate shipping
    grand_total = cart_total + tax + shipping
    
    return render(request, "payment/checkout.html", {
        "cart_products": cart_products, 
        "quantities": quantities, 
        "cart_total": cart_total,
        "tax": tax,
        "shipping": shipping,
        "grand_total": grand_total
    })

def payment_success(request):
    return render(request, "payment/payment_success.html", {})


