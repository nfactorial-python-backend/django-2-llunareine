from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from rest_framework import generics
from rest_framework.decorators import api_view

from .models import News, Comments
from django.http import HttpResponse, HttpResponseRedirect

from .serializers import NewsSerializer


from .forms import NewsForm, SignUpForm
from django.views import View
from django.contrib.auth import login
from django.contrib.auth.models import Group


def index(request):
    news_list = News.objects.order_by('-created_at')
    return render(request, 'news/index.html', {'news_list': news_list})



def news_detail(request, news_id):
    news = get_object_or_404(News, pk=news_id)
    comments = Comments.objects.filter(news=news).order_by('-created_at')

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            comment = Comments(news=news, content=content, created_at=timezone.now(), author=request.user)
            comment.save()
            return redirect('news:news_detail', news_id=news_id)

    return render(request, 'news/detail.html', {'news': news,  'comments': comments})


@login_required(login_url="/login/")
@permission_required("news.add_news", login_url="/login/")
def add_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            return HttpResponseRedirect(reverse('news:news_detail', args=(news.pk,)))
    else:
        form = NewsForm()
    return render(request, 'news/news_create.html', {'form': form})



class NewsUpdateView(View):
    @method_decorator(login_required(login_url="/login/"))

    def get(self, request, news_id):
        news = get_object_or_404(News, pk=news_id)
        form = NewsForm(instance=news)
        return render(request, "news/news_update.html", {'form': form, 'news': news})

    @method_decorator(login_required(login_url="/login/"))
    @method_decorator(permission_required("news.add_news", login_url="/login/"))
    def post(self, request, news_id):
        news = get_object_or_404(News, pk=news_id)
        if request.user == news.author:
            form = NewsForm(request.POST, instance=news)
            if form.is_valid():
                form.save()
                return redirect('news:news_detail', news_id=news_id)
        return HttpResponseRedirect(reverse("news:news_detail", args=(news_id,)))



@login_required(login_url="/login/")
@permission_required('news.delete_news')
def delete_news(request, news_id):
    news = get_object_or_404(News, pk=news_id)
    if request.method == "POST":
        if request.user == news.author or request.user.has_perm("news.delete_news"):
            news.delete()

    return redirect(reverse("news:index"))

@login_required(login_url="/login/")
@permission_required('news.delete_news')
def delete_comment(request, comment_id):
    comments = get_object_or_404(Comments, pk=comment_id)
    if request.method == "POST":
        if request.user == comments.author or request.user.has_perm("comments.delete_comments"):
            comments.delete()

    return redirect(reverse("news:index"))


def sign_up(request):
   if request.method == 'POST':
       form = SignUpForm(request.POST)
       if form.is_valid():
           user = form.save()
           group = Group.objects.get(name="default")
           group.user_set.add(user)
           login(request, user)
           return redirect('/news')
   else:
       form = SignUpForm()

   return render(request, 'registration/sign_up.html', {"form": form})



class  NewsAddView(generics.ListCreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

class NewsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

