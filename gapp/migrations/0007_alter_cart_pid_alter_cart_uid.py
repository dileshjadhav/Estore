# Generated by Django 4.2.3 on 2023-07-20 14:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gapp', '0006_cart_pid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='pid',
            field=models.ForeignKey(db_column='pid', on_delete=django.db.models.deletion.CASCADE, to='gapp.product'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='uid',
            field=models.ForeignKey(db_column='uid', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
