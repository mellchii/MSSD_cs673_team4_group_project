# Generated by Django 3.2.15 on 2022-09-29 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pscmodels', '0007_alter_posts_upvotes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='posts',
            name='upvotes',
        ),
        migrations.AddField(
            model_name='posts',
            name='upvotes',
            field=models.IntegerField(default=0),
        ),
    ]
