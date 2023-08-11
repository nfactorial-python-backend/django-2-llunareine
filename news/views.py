from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone

from .models import News, Comments
from django.http import HttpResponse, HttpResponseRedirect


def index(request):
    news_list = News.objects.order_by('-created_at')
    return render(request, 'news/index.html', {'news_list': news_list})

def news_detail(request, news_id):
    news = get_object_or_404(News, pk=news_id)
    comments = Comments.objects.filter(news=news).order_by('-created_at')

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            comment = Comments(news=news, content=content, created_at=timezone.now())
            comment.save()
            return redirect('news:news_detail', news_id=news_id)

    return render(request, 'news/detail.html', {'news': news,  'comments': comments})


def add_news(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        if title and content:
            news = News(title=title, content=content, created_at=timezone.now())
            news.save()
            return HttpResponseRedirect(reverse('news:news_detail', args=(news.pk,)))

    return render(request, 'news/news_create.html')


