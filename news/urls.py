from django.urls import path

from . import views
app_name = 'news'

urlpatterns = [
    path("", views.index, name="index"),
    path('<int:news_id>/', views.news_detail, name='news_detail'),
    path('add/', views.add_news, name='add_news'),
]
