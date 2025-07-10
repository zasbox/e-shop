from django.db import models

# Create your models here.
NULLABLE = {'blank': True, 'null': True}


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='наименование')
    description = models.TextField(verbose_name='описание', **NULLABLE)
    preview = models.ImageField(upload_to='products/', verbose_name='превью')
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    price = models.IntegerField(verbose_name='цена')
    created_at = models.DateField(verbose_name='дата создания', auto_now_add=True)
    modificated_at = models.DateField(verbose_name='дата изменения', auto_now=True)
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, verbose_name='Пользователь', **NULLABLE)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ['pk']


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    created_at = models.DateField(verbose_name='дата создания', auto_now_add=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Version(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    number = models.IntegerField(verbose_name='номер')
    title = models.CharField(max_length=50, verbose_name='название')
    is_currency = models.BooleanField(verbose_name='текущая', default=False)

    def __str__(self):
        return f'{self.title} {self.number}'

    class Meta:
        verbose_name = 'версия'
        verbose_name_plural = 'версии'

