from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
from .utils import unique_slug_generator

User = get_user_model()

class Category(models.Model):
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class CustomManager(models.Manager):
    # subclass model manager
    def custom_category_dict(self, **kwargs):
        # add a new method for building a dictionary
        nDict = dict()
        for i in self.get_queryset().filter(**kwargs):  # filter queryset based on keyword argument passed to this method
            current_list = nDict.get(i.category.name, [])
            current_list.append(i)
            nDict.update({i.category.name: current_list})
        return nDict


class Post(models.Model):
    class Meta:
        ordering = ['category', '-date_posted']
    # override posts model with manager
    objects = CustomManager()

    author      = models.ForeignKey(User, on_delete=models.CASCADE)
    title       = models.CharField(max_length=60)
    category    = models.ForeignKey(Category, blank=True, null=True, on_delete=models.CASCADE)
    content     = RichTextUploadingField(
                                    external_plugin_resources=[(
                                        'youtube',
                                        '/static/ckeditor/ckeditor/plugins/youtube/',
                                        'plugin.js'
                                        )],
                                        blank=True,
                                        null=True,
                                    )
    date_posted = models.DateTimeField(default=timezone.now)
    updated     = models.DateTimeField(auto_now=True)
    slug        = models.SlugField(max_length=70, blank=True, null=True, help_text='<font color="red">don\'t. touch. the. slug. field. unless. you. mean. it.</font> (it will auto-generate, don\'t worry.)')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # return reverse('blog:post-detail', kwargs={'pk': self.pk})
        return reverse('blog:post-detail', kwargs={'slug': self.slug})


class Comment(models.Model):
    post                = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author              = models.ForeignKey(User, on_delete=models.CASCADE)
    text                = models.TextField()
    created_date        = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text


def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(pre_save_receiver, sender=Post)
