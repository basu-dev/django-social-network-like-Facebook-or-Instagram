from django.http import JsonResponse
from stories.models import *
from message.models import Message_Notification

def like(request,id):
    if request.is_ajax:
        if request.method == 'POST':
            post=Post.objects.get(id= id)
            like=Like.objects.filter(post=post).filter(user=request.user)
            if like:
                like.delete()
                count=Like.objects.filter(post=post).count()
                truth='True'
                is_liked='Like'
            else:
                like=Like()
                like.user=request.user
                like.post=post
                like.like=True
                like.save()
                count=Like.objects.filter(post=post).count()
                truth='False'
                is_liked='Liked'
            return JsonResponse({'count':count,'truth':truth,'is_liked':is_liked})

def comment(request,id):
    if request.method=='POST':
        comment = request.POST['comment']
        new_cmt = Comment()
        new_cmt.body= comment
        new_cmt.user =  request.user
        new_cmt.post  = Post.objects.get(id = id)
        if comment:
            new_cmt.save()
            data={"comment":comment,"user":request.user.first_name,"profile_picture":request.user.profile.profile_picture.url}
            return JsonResponse(data)

def messagecheck(request):
    new_message=Message_Notification.objects.filter(receiver=request.user.id)[0]
    user=User.objects.get(id=new_message.sender)
    u_id=request.user.id
    id=new_message.sender
    get_last_message=Message.objects.filter(Q(sender=u_id)|Q(receiver=u_id)).filter(Q(sender=id)|Q(receiver=id)).exclude(Q(del_by_sender = u_id)|Q(del_by_receiver=u_id)).filter(seen=False).last()
