# Generated by Django 2.1.1 on 2018-12-30 23:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0017_auto_20181230_2239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallery',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Profile'),
        ),
    ]
