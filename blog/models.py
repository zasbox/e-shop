from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=150, verbose_name='заголовок')
    slug = models.CharField(verbose_name='slag')
    text = models.TextField(verbose_name='содержимое')
    preview = models.ImageField(upload_to='previews/', verbose_name='превью', blank=True, null=True)
    created_at = models.DateField(verbose_name='дата создания', auto_now_add=True)
    is_published = models.BooleanField(verbose_name='Опубликовано', default=False)
    view_count = models.IntegerField(verbose_name='Количество просмотров', default='0')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'