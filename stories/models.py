from django.db import models
from django.contrib.auth.models import User
# from gdstorage.storage import GoogleDriveStorage
import os
# from SocialNetwork.settings import GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE

# Define Google Drive Storage
# print(GoogleDriveStorage)
# gd_storage = GoogleDriveStorage(GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE)

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    storytype= models.TextField(default=" added a story ")
class PostImage(models.Model):
    url=models.ImageField(upload_to="post-images/")
    post=models.ForeignKey(Post,on_delete=models.CASCADE
    )
class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
class PostForUser(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)

def get_comment(post_id):
    post = Post.objects.get(id = post_id)
    comments = Comment.objects.filter(post = post).order_by('-id')[:5]
    return comments

class Like(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    post = models.ForeignKey(Post,on_delete = models.CASCADE)
    like = models.BooleanField(default =False)
def if_liked(request,id):
    is_liked=Like.objects.filter(post=id).filter(user=request.user)
    if is_liked:
        return True
    else:
        return False    
class Notification(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    body = models.TextField()
    seen = models.BooleanField(default=False)
    url=models.CharField(max_length=200,default='loadMyProfile()')
    def make_seen(self):
        self.seen = True
        self.save()
def get_last_ten(user):
    no=Notification.objects.filter(user=user).order_by('-id')[:7]
    return no
def set_notification(user,body,seen,url):
    new_notif=Notification()
    new_notif.user = user
    new_notif.body = body
    new_notif.seen = seen
    new_notif.url=url
    new_notif.save()
def get_stories_user(request,userid):
    stories=Post.objects.filter(user=userid).order_by('-id')[:5]
    if((len(stories)) == 5):
        lastid=stories[len(stories) - 1].id
    else:
        lastid=0
    try:
        firstid=stories[0].id
    except:
        firstid=1000000000000000
    for story in stories:
        story.comment=get_comment(story.id)
        story.like = Like.objects.filter(post = story)
        story.is_liked=if_liked(request,story)    
        story.images=PostImage.objects.filter(post=story)[:2]
    return (stories,lastid,firstid)
def get_more_stories_user(request,userid,lastid,firstid):
    stories=[]
    #logic for more stories
    stories+=Post.objects.filter(user=userid).filter(id__gt=firstid).order_by('-id')
    stories+=Post.objects.filter(user=userid).filter(id__lt=lastid).order_by('-id')[:5]
    if(len(stories) >= 5):
        lastid=stories[len(stories) - 1].id
    else:
        lastid=0
    for story in stories:
        story.comment=get_comment(story.id)
    
        story.like = Like.objects.filter(post = story)
        story.is_liked=if_liked(request,story)
    
        story.images=PostImage.objects.filter(post=story)[:2]
    return (stories,lastid)
def get_stories_all_friends(request,user):
    stories=[]
    posttosee=PostForUser.objects.filter(user=user.id).order_by('-id')[:5]
    if(len(posttosee) >= 5):
        lastid=posttosee[len(posttosee) - 1].id
    else:
        lastid=0
    try:
        firstid=posttosee[0].id
    except:
        firstid=1000000000000000000000000
    for post in posttosee:
        
        stories+=Post.objects.filter(id=post.post.id)
    for story in stories:
        story.comment=get_comment(story.id)
   
        story.like = Like.objects.filter(post = story)
        story.is_liked=if_liked(request,story)
   
        story.images=PostImage.objects.filter(post=story)[:1]
    if(stories==[]):
        stories=get_stories_user(request,1)[0]
    return (stories,lastid,firstid)
def get_more_stories_all(request,user,lastid,firstid):
    stories=[]
    posttosee=[]
    # posttosee=PostForUser.objects.filter(user=user.id).order_by('-id')[5:5]
    newstories=PostForUser.objects.filter(user=user.id).filter(id__gt=firstid).order_by('-id')[:5]
    n=5-len(newstories)
    oldstories=PostForUser.objects.filter(user=user.id).filter(id__lt=lastid).order_by('-id')[:n]
    posttosee+=newstories
    posttosee+=oldstories
    if(len(posttosee)>=5):
        lastid=posttosee[len(posttosee) - 1].id
        if(posttosee[0].id > firstid):
            firstid=posttosee[0].id
    else:
        lastid=0  
    for post in posttosee:
        stories+=Post.objects.filter(id=post.post.id)
    for story in stories:
        story.comment=get_comment(story.id)
   
        story.like = Like.objects.filter(post = story)
        story.is_liked=if_liked(request,story)  
   
        story.images=PostImage.objects.filter(post=story)[:2]

    return (stories,lastid,firstid)
def get_single_story(request,id):

    story=Post.objects.get(id=id)
    story.like=Like.objects.filter(post=story)
    story.is_liked=if_liked(request,story)
    
    story.comment=Comment.objects.filter(post=story)
    story.images=PostImage.objects.filter(post=story)[:2]
    return story
    
def load_more(lastid):
    if (lastid == 0):
        return False
    else:
        return True
