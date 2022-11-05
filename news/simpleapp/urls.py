from django.urls import path
# Импортируем созданные нами представления
from django.views.decorators.cache import cache_page

from .views import NewsList, NewsDetail, NewsSearch, NewsCreate, NewsUpdate, NewsDelete, CategoryList, subscribe, \
   Profile, save_author, like_news,dislike_news

urlpatterns = [
   path('search/', NewsSearch.as_view()),
   path('', cache_page(5)(NewsList.as_view()), name='news_list'),
   path('<int:pk>', NewsDetail.as_view(), name='news_detail'),
   path('<int:pk>/like',like_news , name='like_news'),
   path('<int:pk>/dislike',dislike_news , name='dislike_news'),
   path('create/', NewsCreate.as_view(), name='news_create'),
   path('<int:pk>/update/', NewsUpdate.as_view(), name='news_update'),
   path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
   path('categories/<int:pk>/', cache_page(60*5)(CategoryList.as_view()), name='category_list'),
   path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
   path('profile/', Profile.as_view()),
   path('profile/author', save_author, name='new_author'),

]
