# Generated by Django 4.0 on 2023-10-31 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0003_alter_transaction_categoryfield'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transaction_number',
            field=models.CharField(blank=True, max_length=30, null=True, unique=True),
        ),
    ]
