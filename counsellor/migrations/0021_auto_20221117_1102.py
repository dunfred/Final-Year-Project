# Generated by Django 3.1.4 on 2022-11-17 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('counsellor', '0020_auto_20221117_1053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='availableday',
            name='day',
            field=models.CharField(max_length=15, unique=True, verbose_name='Type'),
        ),
    ]