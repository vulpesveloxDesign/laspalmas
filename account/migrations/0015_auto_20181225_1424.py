# Generated by Django 2.1.1 on 2018-12-25 13:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_auto_20181216_0019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallery',
            name='owner',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
