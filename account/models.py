import os
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image, ImageOps
from ckeditor_uploader.fields import RichTextUploadingField

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_visible = models.BooleanField(null=True)
    activation_key = models.CharField(max_length=120, blank=True, null=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    surname = models.CharField(max_length=30, blank=True, null=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    slogan = models.CharField(max_length=250, blank=True, null=True)
    bio = RichTextUploadingField(
                                external_plugin_resources=[(
                                    'youtube',
                                    '/static/ckeditor/ckeditor/plugins/youtube/',
                                    'plugin.js'
                                    )],
                                    blank=True,
                                    null=True,
                                )
    phone = models.CharField(max_length=20, blank=True, null=True)
    reddit = models.CharField(max_length=30, blank=True, null=True)
    webpage = models.CharField(max_length=30, blank=True, null=True)
    twitter = models.CharField(max_length=30, blank=True, null=True)
    youtube = models.CharField(max_length=30, blank=True, null=True)
    linkdin = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def save(self, force_insert=False, force_update=False, using=None):
        super().save()
        # this part needs expansion.
        img = Image.open(self.image.path)
        if img.width > 300 or img.height > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


def user_directory_path(instance, filename):
    return 'images/{}/{}'.format(instance.owner.user.username, filename)

class Gallery(models.Model):
    class Meta:
        verbose_name = 'gallery'
        verbose_name_plural = 'galleries'

    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    # extra_img = models.ImageField(default='default.jpg', upload_to='images')
    extra_img = models.ImageField(default='default.jpg', upload_to=user_directory_path)

    def __str__(self):
        return '{}'.format(str(self.extra_img)[7:])

    def get_absolute_url(self):
        return reverse('account:view-profile', args=[str(self.owner.username)])

    def save(self, force_insert=False, force_update=False, using=None):
        if not os.path.exists('media/images/thumbs_color/{}'.format(self.owner.user.username)):
            os.makedirs('media/images/thumbs_color/{}'.format(self.owner.user.username))
            os.makedirs('media/images/thumbs_bw/{}'.format(self.owner.user.username))
            print('NEW FOLDERS ADDED!')
        try:
            super().save()
            img = Image.open(self.extra_img.path)
            # if img.width > 900 or img.height > 900:
            if img.width > 900 and img.height > 900:
                output_size = (900, 900)
                img.thumbnail(output_size)  # not thumbnail, broth!
                img.save(self.extra_img.path)
            xpad = int(img.width/2)-90
            ypad = int(img.height/2)-90
            coords = (xpad, ypad, xpad+90, ypad+90)
            crop_img_color = img.crop(coords)
            color_url = 'media/images/thumbs_color/{0}'.format(str(self.extra_img)[7:])
            crop_img_color = crop_img_color.convert('RGB')
            crop_img_color.save(color_url)
            print('SAVED!')
            bw_url = 'media/images/thumbs_bw/{0}'.format(str(self.extra_img)[7:])
            crop_img_bw = ImageOps.grayscale(crop_img_color)
            crop_img_bw = crop_img_bw.convert('L')
            crop_img_bw.save(bw_url)
            print('WITH BELLS ON!')
        except:
            print('NOT CREATING NEW THUMBNAILS MAKES ME CRANKY!')
