from django.urls import path

from . import views

urlpatterns = [
    path('<str:news_id>', views.news, name='news'),
    path('', views.all_news, name='all_news'),
    path('add/news', views.news_add, name='news_add'),
]