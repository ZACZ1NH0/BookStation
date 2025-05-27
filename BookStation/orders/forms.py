from django import forms
from .models import Order, OrderItem
from django.forms import inlineformset_factory

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['note']
        widgets = {
            'note': forms.Textarea(attrs={'rows': 3}),
        }

# Tạo formset để thêm nhiều OrderItem vào 1 Order
OrderItemFormSet = inlineformset_factory(
    Order,
    OrderItem,
    fields=['book', 'quantity'],
    extra=1,
    can_delete=True,
    widgets={
        'quantity': forms.NumberInput(attrs={'min': 1})
    }
)
