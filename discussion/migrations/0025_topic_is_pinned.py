# Generated by Django 2.2.16 on 2020-10-06 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0024_auto_20200814_1043'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='is_pinned',
            field=models.BooleanField(default=False, verbose_name='pinned'),
        ),
    ]