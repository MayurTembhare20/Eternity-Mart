from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from order.models import Order, Order_Details,Payment
from django.views.decorators.csrf import csrf_exempt
from product.models import Products
from .forms import Place_Order_Form
from datetime import datetime
from .models import Cart
from django import views
import razorpay
import json


@login_required
def add_to_cart_view(request):
    """ Handle add to cart form """
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        variation_id = request.POST.get('variation_id')
        product_id = request.POST.get('product_id')
        product = Products.objects.get(id=product_id)
        cart, is_created = Cart.objects.get_or_create(user=request.user, product_id=product_id, variation_id=variation_id)
        """get_or_create() : Either it will create object with kwargs or fetch object with given kwargs """
        cart.quantity = quantity
        cart.save()
        return redirect('my_cart_view')

    return redirect('home_page')


@login_required
def my_cart_view(request):
    """ Display list of products from cart """
    cart_products = Cart.objects.filter(user=request.user)
    sub_total = 0
    shipping = 50
    for cart_product in cart_products:
        cart_product.sub_total = cart_product.product.price * cart_product.quantity
        sub_total = sub_total + cart_product.sub_total
    grand_total = sub_total + shipping
    context = {
        'cart_products' : cart_products,
        'sub_total' : sub_total,
        'shipping' : shipping,
        'grand_total' : grand_total,
    }
    return render(request, 'cart/my_cart.html', context)


@login_required
def delete_cart_item_view(request, cart_id):
    """ Delete an item from my cart """
    try:
        Cart.objects.get(id=cart_id).delete()
    except Cart.DoesNotExist:
        pass
    return redirect('my_cart_view')


@method_decorator(login_required, name="dispatch")
class Checkout(views.View):
    """ Checkout to my cart """
    template_name =  'cart/checkout.html'

    def get(self,request):
        initial = {
            'address' : request.user.user_profile.address,
            'mobile' : request.user.user_profile.mobile,
        }
        form = Place_Order_Form(request.POST or None, initial=initial)
        cart_products = Cart.objects.filter(user=request.user)
        sub_total = 0
        shipping = 50
        for cart_product in cart_products:
            cart_product.sub_total = cart_product.product.price * cart_product.quantity
            sub_total = sub_total + cart_product.sub_total

        if sub_total < 500 :
            shipping = 0
        grand_total = sub_total + shipping

        context = {
            'form' : form,
            'sub_total' : sub_total,
            'shipping' : shipping,
            'grand_total' : grand_total,
        }
        return render(request,self.template_name,context)

    def post(self,request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.user.user_profile.address
        initial = {
            'address' : request.user.user_profile.address,
            'mobile' : request.user.user_profile.mobile,
        }
        """ Form Handling """
        form = Place_Order_Form(request.POST or None, initial=initial)
        cart_products = Cart.objects.filter(user=request.user)
        sub_total = 0
        shipping = 50

        for cart_product in cart_products:
            cart_product.sub_total = cart_product.product.price * cart_product.quantity
            sub_total = sub_total + cart_product.sub_total

        if sub_total < 500 :
            shipping = 0
        grand_total = int((sub_total + shipping) * 100)

        client = razorpay.Client(auth=("rzp_test_YzUUNlJWgsB9kq", "pfhjUCm80HMYdWvTLweEb9yE"))
        receipt = f"order_rcptid(request.user.id)"
        data = { "amount": grand_total, "currency": "INR", "receipt": receipt }
        payment = client.order.create(data=data)
        
        if payment.get('id'):  
            if form.is_valid():
                mobile = form.cleaned_data.get('mobile')
                address = form.cleaned_data.get('address')
                order = Order.objects.create(
                    user=request.user,
                    date_time=datetime.now(),
                    address=address,
                    mobile=mobile,
                 )          

            context = {
                    'order_id' : payment['id'],
                    'amount' : payment['amount'],
                    'first_name': first_name,
                    'last_name' : last_name,
                    'address' : address,
                    'mobile' : mobile
                    } 
            
            return render(request,'cart/capture_payment.html',context)
        else:
            return render(request,'error.html')
    

class payment_successs(views.View):
    """ Payment Handling """
    def post(self,request):
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_signature = request.POST.get('razorpay_signature')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        cart_products = Cart.objects.filter(user=request.user)

        if cart_products:
            order= Order.objects.create(
                user = request.user,
                date_time = datetime.now(),
                address = address,
                razor_pay_order_id = razorpay_order_id
            )
            for cart_product in cart_products:
                """ Processing cart to create order details """
                Order_Details.objects.create(
                        order = order,
                        product = cart_product.product,
                        quantity = cart_product.quantity,
                        price = cart_product.product.price,
                        variation = cart_product.variation,
                )
            cart_products.delete()

        return JsonResponse({'status':'success'})


@csrf_exempt
def RazorpayWebhook(request):
    """ Processing Webhook to create payment details and responses """
    requestBody = json.loads(request.body.decode("utf-8"))
    payload = requestBody['payload']
    if payload['payment']:
        order_id = payload['payment']['entity']['order_id']
        if order_id:
            order = Order.objects.get(razor_pay_order_id = order_id) 
            pay = Payment.objects.create(order = order)
            pay.Payment_id = payload['payment']['entity']['id']
            pay.Payment_status = payload['payment']['entity']['status']
            pay.Payment_method = payload['payment']['entity']['method']
            pay.created_at = payload['payment']['entity']['created_at']
            pay.amount = payload['payment']['entity']['amount']
            pay.save() 
            order.payment_status = True
            order.status = "success"
            order.save()       
            return JsonResponse({'status':'success'})
        else:
            return JsonResponse({'status':'failed'})


def thank_you_view(request):
    """ Create thank you view """
    return render(request, 'cart/thank_you.html')