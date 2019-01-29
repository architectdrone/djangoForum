from django.db import models

# Create your models here.

class user(models.Model):
    name = models.CharField(max_length = 20)
    posts_made = models.ManyToManyField('post', related_name = 'user_posts')
    comments_made = models.ManyToManyField('comment', related_name = 'user_comments')
    def __str__(self):
        return self.name

class post(models.Model):
    user = models.ForeignKey('user', related_name = 'poster', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now = True)
    subject = models.CharField(max_length = 100)
    content = models.CharField(max_length = 2000)
    replies = models.ManyToManyField('comment', related_name = 'post_replies')
    def __str__(self):
        return self.subject

class comment(models.Model):
    user = models.ForeignKey('user', related_name = 'commenter', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now = True)
    content = models.CharField(max_length = 2000)
    post = models.ForeignKey('post', related_name = 'associated_post', on_delete=models.CASCADE)
    def __str__(self):
        return self.post
