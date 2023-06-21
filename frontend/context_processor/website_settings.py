from cms.models import Website_Setting
from cart.models import Cart

def website_setting(request):
    """ Website setting, Display dynamic LOGO, TITLE and address details on frontend """
    website_setting = Website_Setting.objects.all().last()
    return { 'global_website_setting' : website_setting }


def cart_count(request):
    """ Display cart count on website header """
    quantity = 0
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user)
        for cart in carts:
            quantity = quantity + cart.quantity
    return {'global_cart_quantity' : quantity}
