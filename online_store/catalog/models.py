from django.db import models
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE_CASCADE


class Category(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    name = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    article_number = models.CharField(max_length=50, unique=True)
    price = models.FloatField()
    stock = models.PositiveIntegerField(default=0)
    image_url = models.URLField()

    def __str__(self):
        return f'{self.name} | stock: {self.stock}'
