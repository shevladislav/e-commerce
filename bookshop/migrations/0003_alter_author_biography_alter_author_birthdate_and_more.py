# Generated by Django 4.0.5 on 2022-06-29 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookshop', '0002_author_bookseries_illustrator_interpreter_publisher_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='biography',
            field=models.TextField(blank=True, null=True, verbose_name='Біографія'),
        ),
        migrations.AlterField(
            model_name='author',
            name='birthdate',
            field=models.DateField(blank=True, null=True, verbose_name='Дата народження'),
        ),
        migrations.AlterField(
            model_name='author',
            name='death_date',
            field=models.DateField(blank=True, null=True, verbose_name='Дата смерті'),
        ),
        migrations.AlterField(
            model_name='author',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='img', verbose_name='Фото'),
        ),
    ]
