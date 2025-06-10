from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from .models import Order, OrderItem
from books.models import Book
from .forms import OrderForm, OrderItemFormSet


# @login_required
# def create_order(request):
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         formset = OrderItemFormSet(request.POST)

#         if form.is_valid() and formset.is_valid():
#             order = form.save(commit=False)
#             order.customer = request.user
#             order.save()

#             order_items = formset.save(commit=False)
#             for item in order_items:
#                 item.order = order
#                 item.save()

#             return redirect('order_success')  
#     else:
#         form = OrderForm()
#         formset = OrderItemFormSet()

#     return render(request, 'orders/create_order.html', {
#         'form': form,
#         'formset': formset
#     })

def create_order(request):
    cart = request.session.get("cart", {})
    selected_keys = request.POST.getlist("selected_items") if request.method == 'POST' else list(cart.keys())
    selected_cart = {}
    total = 0

    for key in selected_keys:
        if key in cart:
            item = cart[key]
            subtotal = float(item["price"]) * int(item["quantity"])
            item["subtotal"] = subtotal
            selected_cart[key] = item
            total += subtotal

    if request.method == 'POST' and selected_cart:
        # Lưu đơn hàng
        order = Order.objects.create(customer=request.user, note=request.POST.get('note', ''))
        from books.models import Book
        for key, item in selected_cart.items():
            OrderItem.objects.create(
                order=order,
                book_id=key,
                quantity=item['quantity'],
                price=item['price']
            )
            # Giảm tồn kho sách
            try:
                book = Book.objects.get(pk=key)
                book.stock = max(0, book.stock - int(item['quantity']))
                book.save()
            except Book.DoesNotExist:
                pass
        request.session['cart'] = {}
        return redirect('order_success')

    form = OrderForm()
    return render(request, "orders/create_order.html", {
        "form": form,
        "cart": selected_cart,
        "total": total,
    })


@login_required
def add_to_cart(request, pk):
    from django.contrib import messages
    book = get_object_or_404(Book, pk=pk)
    if book.stock == 0:
        messages.error(request, 'Sách này tạm thời hết hàng, không thể thêm vào giỏ.')
        return redirect('book_detail', pk=pk)
    cart = request.session.get('cart', {})
    quantity = int(request.POST.get('quantity', 1))
    if str(pk) in cart:
        cart[str(pk)]['quantity'] += quantity
    else:
        cart[str(pk)] = {
            # 'image': book.cover_image,
            'title': book.title,
            'price': float(book.price),
            'quantity': quantity
        }

    request.session['cart'] = cart
    return redirect('view_cart')

@login_required
def view_cart(request):
    cart = request.session.get('cart', {})
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    for item in cart.values():
        item['subtotal'] = item['price'] * item['quantity']
    return render(request, 'orders/cart.html', {
        'cart': cart,
        'total': total
        
    })


@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('view_cart')

    total = sum(Decimal(item['price']) * item['quantity'] for item in cart.values())
    order = Order.objects.create(customer=request.user, total_amount=total)

    for book_id, item in cart.items():
        OrderItem.objects.create(
            order=order,
            book_id=book_id,
            quantity=item['quantity'],
            price=item['price']
        )

    # Xóa giỏ hàng sau khi thanh toán
    request.session['cart'] = {}
    return redirect('home')

def order_success(request):
    return render(request, 'orders/order_success.html')

@login_required
def order_list(request):
    orders = Order.objects.filter(customer=request.user).prefetch_related('items__book').order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})
