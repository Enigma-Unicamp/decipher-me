# Generated by Django 2.1.4 on 2019-01-23 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0014_auto_20190117_1444'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='points',
            field=models.PositiveIntegerField(default=None),
            preserve_default=False,
        ),
    ]
