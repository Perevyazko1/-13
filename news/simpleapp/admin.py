from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Author, Comment, News, NewsCategory


def nullfy_rating(modeladmin, request,
                    queryset):  # request — объект хранящий информацию о запросе и queryset — грубо говоря набор
    # объектов, которых мы выделили галочками.
    for object in queryset.values('rating'):
        print(object)

nullfy_rating.short_description = 'Обнулить лайки'  # описание для более понятного представления в админ панеле
# задаётся, как будто это объект


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('authorUser', 'ratingAuthor')  # оставляем только имя и цену товара


# создаём новый класс для представления товаров в админке
class NewsAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('dateCreation', 'title', 'author', 'total_likes', 'get_image')  # оставляем только имя и цену товара
    list_filter = ('dateCreation', 'author')  # добавляем примитивные фильтры в нашу админку
    search_fields = ('title', 'text')  # тут всё очень похоже на фильтры из запросов в базу


    def get_image (self, object):
        return mark_safe (f'<img src = "{object.image.url}" width=50')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('dateCreation', 'commentPost', 'commentUser', 'text', 'total_likes_comment')
    list_filter = ('dateCreation', 'commentUser')
    search_fields = ['text']
    actions = [nullfy_rating]  # добавляем действия в список

admin.site.register(News, NewsAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(NewsCategory)


admin.site.site_title = 'Админ панель News Portal'