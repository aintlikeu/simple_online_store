from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    # CATEGORY_CHOICES = [
    #     ('TS', 'T-shirts'),
    #     ('SW', 'Sweatshirts'),
    #     ('PN', 'Pants'),
    #     ('JC', 'Jackets'),
    # ]

    name = models.CharField(max_length=150)
    # category = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=None)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    article_number = models.CharField(max_length=50, unique=True)
    price = models.FloatField()
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='images/catalog')

    def __str__(self):
        return f'{self.name} | stock: {self.stock}'
