# Generated by Django 3.2.15 on 2022-09-29 06:11

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pscmodels', '0006_auto_20220929_0528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='upvotes',
            field=models.ManyToManyField(related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
    ]