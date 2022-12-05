from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum, Count
from django.urls import reverse


def get_full_name(self):
    if self.last_name:
        return f'{self.last_name} {self.first_name}'
    else:
        return f'{self.username}'


User.add_to_class("__str__", get_full_name)


# class User(auth.models.User):
#     def __str__(self):
#         if self.last_name:
#             return f'{self.last_name} {self.first_name}'
#         else:
#             return f'{self.username}'


class Author(models.Model):
    class Meta:
        verbose_name = u"Автор"
        verbose_name_plural = u"Авторы"

    authorUser = models.OneToOneField(User, on_delete=models.CASCADE, default=1, blank=True,
                                      verbose_name='Пользователь')

    ratingAuthor = models.SmallIntegerField(default=0)

    def rating_author(self):
        return self.news_set.aggregate(Count('rating')).get('rating__count')

        # post_rating = self.news_set.aggregate(Sum('rating')).get('rating__sum')
        # if post_rating is None:
        #     post_rating = 0
        #
        # comment_rating = self.authorUser.comment_set.aggregate(Sum('rating')).get('rating__sum')
        # if comment_rating is None:
        #     comment_rating = 0
        #
        # compost_rating = 0
        # for post in self.post_set.all():
        #     rating = post.comment_set.aggregate(Sum('rating')).get('rating__sum')
        #     if rating is None:
        #         rating = 0
        #     compost_rating += rating
        #
        # self.ratingAuthor = post_rating * 3 + comment_rating + compost_rating
        # self.save()

    def __str__(self):
        if self.authorUser.last_name:
            return f'{self.authorUser.last_name} {self.authorUser.first_name}'
        else:
            return f'{self.authorUser.username}'


class NewsCategory(models.Model):
    class Meta:
        verbose_name = u"Категория новости"
        verbose_name_plural = u"Категории новостей"

    name = models.CharField(max_length=100, unique=True, default=None)
    subscribes = models.ManyToManyField(User, related_name='categories')

    def __str__(self):
        return self.name


# Create your models here.
class News(models.Model):
    class Meta:
        verbose_name = u"Новость"
        verbose_name_plural = u"Новости"

    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')
    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья')
    )
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES,
                                    default=ARTICLE, verbose_name='Тип')
    dateCreation = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    # category = models.ForeignKey(
    #     to='NewsCategory',
    #     on_delete=models.CASCADE,
    #     related_name='news',
    #     verbose_name='Категория'# все продукты в категории будут доступны через поле news
    # )
    category = models.ManyToManyField(NewsCategory, through='Postcategory')
    title = models.CharField(max_length=128, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    rating = models.ManyToManyField(User, related_name='rating')
    image = models.ImageField(upload_to='images/', default=None)
    ordering = ['-dateCreation']

    def total_likes(self):
        return self.rating.count()

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])

    def preview(self):
        preview = self.text[0:124] + '...'
        return preview

    def __str__(self):
        return f'{self.title}| {self.text[:20]}'


class PostCategory(models.Model):
    postThrough = models.ForeignKey(News, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(NewsCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.postThrough.title()} | {self.categoryThrough.name}'


class Comment(models.Model):
    class Meta:
        verbose_name = u"Комментарий к новости"
        verbose_name_plural = u"Комментарии к новостям"

    commentPost = models.ForeignKey(News, on_delete=models.CASCADE, verbose_name='Новость')
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    text = models.TextField(verbose_name='Комментарий')
    dateCreation = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    rating = models.ManyToManyField(User, related_name='rating_comment')

    def total_likes_comment(self):
        return self.rating.count()

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.commentPost.id)])

    def delete_likes(self):
        return self.rating.update(quantity=0)
