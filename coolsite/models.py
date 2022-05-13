from django.contrib.auth.models import User, AbstractUser
from django.db import models
from PIL import Image
from django.urls import reverse

class Posts(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    photo = models.ImageField(default='default.jpg', verbose_name='Фото' )
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def get_absolute_url(self):
        return reverse('show-post', kwargs={'slug':self.slug})

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    status = models.TextField(max_length=400)
    bio = models.TextField()

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)

class Friend(models.Model):
    friend1 = models.ForeignKey('Profile', blank=True, related_name='friend1', on_delete=models.CASCADE,null=True)
    friend2 = models.ForeignKey('Profile', blank=True, related_name='friend2',on_delete=models.CASCADE,null=True)

    class Meta:
        verbose_name = 'Друг'
        verbose_name_plural = 'Друзья'