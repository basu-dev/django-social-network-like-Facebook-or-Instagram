from stories.models import Post
from django.http import JsonResponse

def delete(request,id):
    if request.method=='POST':
        story = Post.objects.get(id=id)
        story.delete()
        return JsonResponse({'success':"successful"})