from django import forms
from .models import Book, Category, Author, Publisher

class BookForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Categories"
    )

    class Meta:
        model = Book
        fields = [
            'title', 'price', 'description', 'stock', 'cover_image',
            'publication_date', 'author', 'publisher', 'categories'
        ]
        widgets = {
            'publication_date': forms.DateInput(attrs={'type': 'date'}),
        }

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'bio', 'image', 'nationality', 'birth_date']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

class PublisherForm(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = ['name', 'address', 'email']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

