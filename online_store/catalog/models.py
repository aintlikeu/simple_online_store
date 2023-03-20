from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):

    name = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    article_number = models.CharField(max_length=50, unique=True)
    price = models.FloatField()
    stock = models.PositiveIntegerField(default=0)
    image_url = models.URLField()

    def __str__(self):
        return f'{self.name} | stock: {self.stock}'
