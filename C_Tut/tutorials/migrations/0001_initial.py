# Generated by Django 2.1.7 on 2019-04-23 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tutorial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('html_name', models.CharField(max_length=300)),
                ('created_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
    ]
