# Generated by Django 4.0 on 2023-11-17 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0006_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
