from django import template

register = template.Library()

@register.filter(name="isexistsincart")
def isexistsincart(product,cart):
    keys = cart.keys()
    for key in keys:
        if int(key)==product.id:
            return True
    return False

@register.filter(name="cartquantity")
def cartquantity(product,cart):
    keys = cart.keys()
    for key in keys:
        if int(key)==product.id:
            return cart.get(key)
    return 

@register.filter(name="total_price")
def total_price(product, cart):
    tp = product.product_price * cartquantity(product,cart)
    return tp

@register.filter(name="payable_amount")
def payable_amount(product,cart):
    s=0
    for i in product:
        s = s + total_price(i,cart)
    return s

@register.filter(name = "total_price_order")
def total_price_order(price,quantity):
    return price*quantity