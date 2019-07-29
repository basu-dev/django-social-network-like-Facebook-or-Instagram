from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)


def get_comment(post_id):
    post = Post.objects.get(id = post_id)
    comments = Comment.objects.filter(post = post)
    return comments

class Like(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    post = models.ForeignKey(Post,on_delete = models.CASCADE)
    like = models.BooleanField(default =False)
    def if_liked(request,id):
        is_liked=Like.objects.filter(post=id).filter(user=request.user)
        if is_liked:
            return 'True'
        else:
            return 'False'    
class Notification(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    body = models.TextField()
    seen = models.BooleanField(default=False)
    url=models.CharField(max_length=200,default='/profile/')
    def make_seen(self):
        self.seen = True
        self.save()
def get_last_ten(user):
    no=Notification.objects.filter(user=user).order_by('-id')[:10]
    return no

def set_notification(user,body,seen,url):
    new_notif=Notification()
    new_notif.user = user
    new_notif.body = body
    new_notif.seen = seen
    new_notif.url=url
    new_notif.save()

