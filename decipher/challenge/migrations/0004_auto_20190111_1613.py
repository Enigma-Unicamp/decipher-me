# Generated by Django 2.1.4 on 2019-01-11 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0003_auto_20190111_1605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='last_capture',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
