# Generated by Django 2.1.4 on 2019-01-12 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0011_challenge_type_chall'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='file_path',
            field=models.TextField(default=None),
            preserve_default=False,
        ),
    ]
