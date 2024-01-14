from django.contrib import messages
from django.shortcuts import render
from App_Order.models import Order
from App_Payment.forms import BillingAddress, BillingAddressForm
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required
def checkout(request):
    saved_address = BillingAddress.objects.get_or_create(user=request.user)[0]
    form = BillingAddressForm(instance=saved_address)
    if request.method == 'POST':
        form = BillingAddressForm(request.POST, instance=saved_address)
        if form.is_valid():
            form.save()
            form = BillingAddressForm(instance=saved_address)
            messages.success(request, f'Shipping Address Successfully Saved')
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order_items = order_qs[0].order_items.all()
    order_total = order_qs[0].get_totals()
    return render(request, 'App_Payment/checkout.html',
                  context={'form': form, 'order_items': order_items, 'order_total': order_total})
