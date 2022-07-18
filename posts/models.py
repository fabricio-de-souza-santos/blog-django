import imp
from pickletools import optimize
from django.db import models
from categorias.models import Categoria
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from PIL import Image
import os


class Post(models.Model):
    titulo_post = models.CharField(max_length=255)
    autor_post = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    data_post = models.DateTimeField(default=timezone.now)
    conteudo_post = models.TextField()
    excerto_post = models.TextField()
    categoria_post = models.ForeignKey(
        Categoria, on_delete=models.DO_NOTHING, blank=True, null=True)
    imagem_post = models.ImageField(
        upload_to='post_img/%Y/%m/', blank=True, null=True)
    publicado_post = models.BooleanField(default=False)

    def __str__(self):
        return self.titulo_post
    
    def save(self,*args, **kwargs):
        super.save(args,kwargs)

        self.resize_image(self.imagem_post.name,800)

    @staticmethod
    def resize_image(nome_image,new_width):
        img_path = os.path.join(settings.MEDIA_ROOT, nome_image)
        img = Image.open(img_path)
        width,height = img.size

        if width <= new_width:
            img.close()
            return

        new_height = round((new_width* height)/width)
        nova_img  = img.resize((new_width, new_height), Image.ANTIALIAS)

        nova_img.save(img_path,optimize=True, quality = 60)
