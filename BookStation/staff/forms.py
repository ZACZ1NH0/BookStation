# from django.contrib.auth.forms import UserCreationForm
from accounts.models import Users
from django import forms
from books.models import Book
from django import forms
from orders.forms import OrderForm
from orders.models import Order
from orders.forms import OrderItemFormSet as BaseOrderItemFormSet


class BookImportForm(forms.Form):
    json_file = forms.FileField(label="File JSON chứa thông tin sách", required=True)
    image_zip = forms.FileField(label="File ZIP chứa ảnh bìa sách", required=True)


class StaffOrderForm(OrderForm):
    class Meta(OrderForm.Meta):
        fields = ['status', 'note']  # Thêm status
        widgets = {
            'status': forms.Select(attrs={'class': 'w-full p-2 border rounded'}),
            'note': forms.Textarea(attrs={'rows': 3, 'class': 'w-full p-2 border rounded'}),
        }

class StaffOrderItemFormSet(BaseOrderItemFormSet):
    def clean(self):
        super().clean()
        for form in self.forms:
            if not form.cleaned_data.get('DELETE'):
                book = form.cleaned_data.get('book')
                quantity = form.cleaned_data.get('quantity')
                if book and quantity and quantity > book.stock:
                    raise forms.ValidationError(f"Sách {book.title} chỉ còn {book.stock} cuốn.")
