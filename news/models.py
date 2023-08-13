from django.db import models

class News(models.Model):
    title = models.CharField(max_length=200, blank=False)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def has_comments(self):
        return Comments.objects.filter(news=self).exists()

class Comments(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


