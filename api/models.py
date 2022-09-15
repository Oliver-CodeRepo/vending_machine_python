from django.db import models

# Create your models here.


# product model 
class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='product name')
    price = models.FloatField(verbose_name='Price value')
    num = models.IntegerField( verbose_name="Number of products")

    def __str__(self):
        return self.name 


# coins model
class Coin(models.Model):
    type = models.CharField(max_length=50, verbose_name='coin type', unique=True)
    value = models.IntegerField(verbose_name='coin value', unique=True)
    num = models.IntegerField(verbose_name='Number of coins')

    def __str__(self):
        return self.type