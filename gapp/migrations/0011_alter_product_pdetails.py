# Generated by Django 4.2.4 on 2023-08-14 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gapp', '0010_contactrecords'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='pdetails',
            field=models.TextField(verbose_name='product details'),
        ),
    ]
