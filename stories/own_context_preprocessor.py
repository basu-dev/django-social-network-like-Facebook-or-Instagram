
from django.conf import settings
def cloudinary_url(request):
    kwargs = {
        'cloudinary_url': settings.CLOUDINARY_URL,
    }
    return kwargs