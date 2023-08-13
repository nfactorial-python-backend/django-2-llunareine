from django.test import TestCase

from django.test import TestCase
from django.urls import reverse
from .models import News, Comments
class NewsModelTests(TestCase):
    def test_has_comments_true(self):
        news = News(title="Test title 1", content="Test content 1")
        news.save()
        comment = Comments(content="Comment 1", news=news)
        comment.save()
        self.assertTrue(news.has_comments())

    def test_has_comments_false(self):
        news = News(title="Test title 2", content="Test content 2")
        news.save()
        self.assertFalse(news.has_comments())


class NewsViewTests(TestCase):
    def test_index(self):
        new1 = News.objects.create(title='Barbie 1', content='Content 1')
        new2 = News.objects.create(title='Barbie 2', content='Content 2')
        new3 = News.objects.create(title='Barbie 3', content='Content 3')

        new1.save()
        new2.save()
        new3.save()

        response = self.client.get(reverse('news:index'))
        news_list = list(response.context['news_list'])
        self.assertEqual(news_list, [new3, new2, new1])

    def test_news_detail(self):
        news = News.objects.create(title='Barbie News', content='Barbie Barbie')
        news.save()
        response = self.client.get(reverse('news:news_detail', args=[news.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['news'].title, news.title)
        self.assertEqual(response.context['news'].content, news.content)

    def test_comments_detail(self):
        news = News.objects.create(title='Barbie News', content='Barbie barbie')
        comment1 = Comments.objects.create(content='Test Comment 1', news=news)
        comment2 = Comments.objects.create(content='Test Comment 2', news=news)
        comment3 = Comments.objects.create(content='Test Comment 3', news=news)

        comment1.save()
        comment2.save()
        comment3.save()

        response = self.client.get(reverse('news:news_detail', args=[news.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['comments']), [comment3, comment2, comment1])

