# Generated by Django 4.2.3 on 2023-07-23 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gapp', '0009_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='contactrecords',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('mobile', models.CharField(default='', max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.CharField(max_length=300)),
            ],
        ),
    ]