from django.shortcuts import render, get_object_or_404, redirect

# authentications
from django.contrib.auth.decorators import login_required

# model
from App_Order.models import Cart, Order
from App_Shop.models import Product

# messages
from django.contrib import messages


# Create your views here.

@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_item = Cart.objects.get_or_create(user=request.user, item=item, purchased=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.order_items.filter(item=item).exists():
            order_item[0].quantity += 1
            order_item[0].save()
            messages.info(request, 'This item quantity was updated.')
            return redirect('App_Shop:index')
        else:
            order.order_items.add(order_item[0])
            messages.info(request, 'This item was added to your cart')
            return redirect('App_Shop:index')
    else:
        order = Order(user=request.user)
        order.save()
        order.order_items.add(order_item[0])
        messages.info(request, 'This item was added to your cart.')
        return redirect('App_Shop:index')


@login_required
def cart_view(request):
    carts = Cart.objects.filter(user=request.user, purchased=False)
    orders = Order.objects.filter(user=request.user, ordered=False)
    if carts.exists() and orders.exists():
        order = orders[0]
        return render(request, 'App_Order/cart.html', {'carts': carts, 'order': order})
    else:
        messages.warning(request, 'You do not have any order in your cart')
        return redirect('App_Shop:index')


@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.order_items.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, purchased=False, user=request.user)[0]
            order.order_items.remove(order_item)
            order_item.delete()
            messages.warning(request, 'This item was removed from your cart')
            return redirect('App_Order:cart')
        else:
            messages.info(request, 'This item is not in your cart.')
            return redirect('App_Shop:index')

    else:
        messages.info(request, 'You don\'t have any orders yet')
        return redirect('App_Shop:index')


@login_required
def increase_quantity(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.order_items.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, purchased=False, user=request.user)[0]
            if order_item.quantity >= 1:
                order_item.quantity += 1
                order_item.save()
                messages.info(request, f'{item.name} quantity has been updated')
                return redirect('App_Order:cart')
            else:
                return redirect('App_Shop:index')
        else:
            messages.info(request, f'{item.name} is not in your cart')
            return redirect('App_Order:cart')
    else:
        messages.info(request, 'You don\'t have any orders yet')
        return redirect('App_Shop:index')


@login_required
def decrease_quantity(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.order_items.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, purchased=False, user=request.user)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                messages.info(request, f'{item.name} quantity has been updated')
                return redirect('App_Order:cart')
            else:
                order.order_items.remove(order_item)
                order_item.delete()
                messages.warning(request, f'{item.name} item has been removed')
                return redirect('App_Order:cart')
        else:
            messages.info(request, f'{item.name} is not in your cart')
            return redirect('App_Order:cart')
    else:
        messages.info(request, 'You don\'t have any orders yet')
        return redirect('App_Order:cart')
