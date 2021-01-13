from django.db import models


def recalc_cart(cart):
    # tą metodą możemy obliczyć, jaka jest ilość towarów i ile jest ogólnie towarów, CartProduct
    # znajdujących się w koszyku.
    cart_data = cart.products.aggregate(models.Sum('final_price'), models.Count('id'))
    if cart_data.get('final_price__sum'):
        cart.final_price = cart_data['final_price__sum']
    else:
        cart.final_price = 0
    cart.total_products = cart_data['id__count']
    cart.save()