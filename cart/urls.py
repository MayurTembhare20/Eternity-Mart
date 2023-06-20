from django.urls import path
from . import views


urlpatterns = [
    path('add-to-cart', views.add_to_cart_view, name="add_to_cart_view"),
    path('my_cart', views.my_cart_view, name="my_cart_view"),
    path('delete_cart_item/<int:cart_id>', views.delete_cart_item_view, name="delete_cart_item_view"),
    path('thank_you', views.thank_you_view, name='thank_you_view'),
    path('Checkout/',views.Checkout.as_view(),name='Checkout'),
    path('payment_successs/',views.payment_successs.as_view(),name='payment_successs'),
    path('webhook',views.RazorpayWebhook),
]