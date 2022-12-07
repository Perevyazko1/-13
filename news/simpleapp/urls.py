from django.urls import path
# Импортируем созданные нами представления
from django.views.decorators.cache import cache_page

from .views import CategoryList, CommentNewsCreate, delete_author, delete_comment, like_comment, \
    like_news, NewsCreate, NewsDelete, NewsDetail, NewsList, NewsSearch, NewsUpdate, Profile, \
    save_author, subscribe

urlpatterns = [
    path('search/', NewsSearch.as_view()),
    path('', cache_page(5)(NewsList.as_view()), name='news_list'),
    path('<int:pk>', NewsDetail.as_view(), name='news_detail'),
    path('<int:pk>/like', like_news, name='like_news'),
    path('<int:pk>/comment', CommentNewsCreate.as_view(), name='comment_news'),
    path('<int:pk>/delete_comment', delete_comment, name='delete_comment'),
    path('<int:pk>/like_comment', like_comment, name='like_comment'),
    path('create/', NewsCreate.as_view(), name='news_create'),
    path('<int:pk>/update/', NewsUpdate.as_view(), name='news_update'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('categories/<int:pk>/', cache_page(60 * 5)(CategoryList.as_view()), name='category_list'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
    path('profile/', Profile.as_view(), name='profile'),
    path('profile/author', save_author, name='new_author'),
    path('profile/delete_author', delete_author, name='delete_author'),

]