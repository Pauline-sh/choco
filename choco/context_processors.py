from .cart import Cart, Gift


def cart(request):
    return {'cart': Cart(request)}


def gift(request):
    return {'gift': Gift(request)}

