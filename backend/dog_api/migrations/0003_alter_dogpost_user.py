# Generated by Django 5.1.4 on 2024-12-31 08:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dog_api', '0002_adoptionapplication_title_alter_dogpost_type'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='dogpost',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dog_posts', to=settings.AUTH_USER_MODEL),
        ),
    ]