from django.db import models


# Товар для нашей витрины
from django.urls import reverse


# Create your models here.
class News(models.Model):
    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья')
    )
    categoryType = models.CharField(max_length=2,choices=CATEGORY_CHOICES,
                                    default=ARTICLE,verbose_name='Тип')
    dateCreation = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    category = models.ForeignKey(
        to='NewsCategory',
        on_delete=models.CASCADE,
        related_name='news',
        verbose_name='Категория'# все продукты в категории будут доступны через поле news
    )
    title = models.CharField(max_length=128, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    def __str__(self):
        return f'{self.title.title()}: {self.text[:20]}'

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])


class NewsCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, default=None)

    def __str__(self):
        return self.name.title()


class PostCategory(models.Model):
    postThrough = models.ForeignKey(News, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(NewsCategory,on_delete=models.CASCADE)