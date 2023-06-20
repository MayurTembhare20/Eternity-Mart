from product.models import Product_Category


def navigation_product_categories(request):
    """ For navigation product category dropdown """
    navigation_product_categories = Product_Category.objects.filter(status=True)
    return { 'navigation_product_categories' : navigation_product_categories }