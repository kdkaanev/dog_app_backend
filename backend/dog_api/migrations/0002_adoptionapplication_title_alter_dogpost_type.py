# Generated by Django 5.1.4 on 2024-12-31 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dog_api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='adoptionapplication',
            name='title',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='dogpost',
            name='type',
            field=models.CharField(choices=[('lost', 'Lost'), ('found', 'Found'), ('adopted', 'Adopted')]),
        ),
    ]
