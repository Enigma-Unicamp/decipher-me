# Generated by Django 2.1.4 on 2019-01-11 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0005_auto_20190111_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='last_capture',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
