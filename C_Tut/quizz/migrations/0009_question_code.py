# Generated by Django 2.1.7 on 2019-05-03 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizz', '0008_auto_20190423_1752'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='code',
            field=models.TextField(blank=True, help_text='code to be solved by user.', max_length=2000, verbose_name='Code'),
        ),
    ]
