import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self, n):
        self.rating += n

    def __str__(self):
        return f'{self.user.username} {self.rating}'


class Category(models.Model):
    category = models.CharField(max_length=70, unique=True)   #модели команы нужно делать, через админку делать почты, умет коммитить и тд + 
    
    def __str__(self):
        return self.category_name


class Post(models.Model):
    author = models.ForeignKey(choices=(
        ('post', 'Post'),
        ('news', 'News'),    
    ))
    create_time = models.DateField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    header = models.TextField()
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.author.update_rating(3)
        self.save()
        self.author.save()

    def dislike(self):
        self.rating -= 1
        self.author.update_rating(-3)
        self.save()
        self.author.save()

    def preview(self):
        if len(self.text) > 124:
            return self.text[:125] + '...'
        else:
            return self.text

    def __str__(self):
        return f'{self.header} {self.rating}'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    create_time = models.DateField(auto_now_add=True)

    def like(self):
        self.rating += 1
        a = Author.objects.filter(user=self.comment_author)[0]
        a.update_rating(1)
        a.save()
        self.post.author.update_rating(1)
        self.save()
        self.post.save()

    def dislike(self):
        self.rating -= 1
        a = Author.objects.filter(user=self.comment_author)[0]
        a.update_rating(-1)
        a.save()
        self.post.author.update_rating(-1)
        self.save()
        self.post.save()

    def __str__(self):
        return f'{self.text} {self.rating}'