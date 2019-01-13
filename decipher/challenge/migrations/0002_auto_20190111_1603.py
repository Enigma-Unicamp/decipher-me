# Generated by Django 2.1.4 on 2019-01-11 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id_chall', models.PositiveIntegerField(primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(max_length=200, unique=True)),
                ('description', models.TextField()),
                ('flag', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='last_capture',
            field=models.DateTimeField(default=None),
        ),
        migrations.AddField(
            model_name='user',
            name='level',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
