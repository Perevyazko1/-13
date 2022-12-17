from .models import News, NewsCategory
from modeltranslation.translator import register, \
    TranslationOptions  # импортируем декоратор для перевода и класс настроек, от которого будем наследоваться


# регистрируем наши модели для перевода

@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('text', 'title')  # указываем, какие именно поля надо переводить в виде кортежа


@register(NewsCategory)
class NewsCategoryTranslationOptions(TranslationOptions):
    fields = ('name',)