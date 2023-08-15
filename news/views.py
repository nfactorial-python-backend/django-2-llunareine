from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone

from .models import News, Comments
from django.http import HttpResponse, HttpResponseRedirect


from .forms import NewsForm

from django.views import View


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
        form = NewsForm(request.POST)
        if form.is_valid():
            news = form.save()
            return HttpResponseRedirect(reverse('news:news_detail', args=(news.pk,)))
    else:
        form = NewsForm()
    return render(request, 'news/news_create.html', {'form': form})



class NewsUpdateView(View):
    template_name = 'news/news_update.html'

    def get(self, request, news_id):
        news = get_object_or_404(News, pk=news_id)
        form = NewsForm(instance=news)
        return render(request, self.template_name, {'form': form, 'news': news})

    def post(self, request, news_id):
        news = get_object_or_404(News, pk=news_id)
        form = NewsForm(request.POST, instance=news)
        if form.is_valid():
            form.save()
            return redirect('news:news_detail', news_id=news_id)
        return render(request, self.template_name, {'form': form, 'news': news})


