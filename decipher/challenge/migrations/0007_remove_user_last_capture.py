# Generated by Django 2.1.4 on 2019-01-11 16:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0006_auto_20190111_1617'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='last_capture',
        ),
    ]
