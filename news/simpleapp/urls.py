from django.urls import path
# Импортируем созданные нами представления
from .views import NewsList, NewsDetail, NewsSearch, NewsCreate, NewsUpdate, NewsDelete

urlpatterns = [
   # path('news/', NewsList.as_view()),
   path('<int:pk>', NewsDetail.as_view()),
   path('search/', NewsSearch.as_view()),
   path('', NewsList.as_view(), name='news_list'),
   path('<int:pk>', NewsDetail.as_view(), name='news_detail'),
   path('create/', NewsCreate.as_view(), name='news_create'),
   path('<int:pk>/update/', NewsUpdate.as_view(), name='news_update'),
   path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
]
