from django.db import models

# Create your models here.

    

class Publisher(models.Model):
    name = models.CharField(max_length=50)
    address = models.TextField()
    email = models.EmailField()

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    image = models.ImageField(upload_to='author/', blank=True, null=True)
    nationality = models.CharField(max_length=40)
    birth_date = models.DateField()

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name



class Book(models.Model):
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)  
    description = models.TextField(blank=True)        
    stock = models.PositiveIntegerField(default=0)    #tồn kho
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)  
    publication_date = models.DateField(null=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, related_name='books')

    def __str__(self):
        return self.title