from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO

from catalog.models import Product


@receiver(post_save, sender=Product)
def optimize_avatar(sender, instance, created, **kwargs):
    if instance.preview and created:
        image = Image.open(instance.preview)
        image = image.convert('RGB')
        image.thumbnail((300, 300))
        img_io = BytesIO()
        image.save(img_io, format='JPEG', quality=85)
        img_io.seek(0)
        file_name = str(instance.preview)
        instance.preview.delete()
        instance.preview = InMemoryUploadedFile(img_io, None, file_name,
                                                'image/jpeg', img_io.getbuffer().nbytes, None)
        instance.save()
