# Generated by Django 4.0.5 on 2022-07-04 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookshop', '0008_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='rating',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Рейтинг'),
        ),
    ]
