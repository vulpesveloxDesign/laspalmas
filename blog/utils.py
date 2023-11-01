# import random
import string
from django.utils.text import slugify
import secrets

DONT_USE = ['create']

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(secrets.choice(chars) for i in range(size))

def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        try:
            slug = slugify(instance.title)
        except:
            slug = slugify(instance.name)
    if slug in DONT_USE:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=4))
    dat_class = instance.__class__
    qs_exists = dat_class.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=4)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug
