# Generated by Django 4.0.6 on 2022-07-18 12:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookshop', '0015_alter_review_options_alter_review_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={},
        ),
        migrations.RemoveField(
            model_name='review',
            name='date',
        ),
    ]
