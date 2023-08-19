from django.urls import path
from .views import NewsUpdateView, NewsDetail
from . import views

from .views import NewsAddView
from django.contrib.auth import views as auth_views

app_name = 'news'

urlpatterns = [
    path("", views.index, name="index"),
    path('<int:news_id>/', views.news_detail, name='news_detail'),
    path('add/', views.add_news, name='add_news'),
    path('<int:news_id>/edit/', NewsUpdateView.as_view(), name='news_update'),
    path('sign-up/', views.sign_up, name='sign_up'),
    path('<int:news_id>/delete/', views.delete_news, name='news_delete'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='comment_delete'),
    path('api/news/', NewsAddView.as_view(), name='news-list'),
    path('api/news/<int:pk>/', NewsDetail.as_view(), name='news-detail'),

]
