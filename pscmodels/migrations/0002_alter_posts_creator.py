# Generated by Django 4.1.1 on 2022-09-26 23:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pscmodels', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='creator',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
