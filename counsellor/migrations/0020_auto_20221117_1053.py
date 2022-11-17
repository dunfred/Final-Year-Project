# Generated by Django 3.1.4 on 2022-11-17 10:53

import counsellor.enums
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('counsellor', '0019_auto_20221116_1209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='counsellor',
            name='title',
            field=models.CharField(choices=[('MR', 'Mr'), ('MRS', 'Mrs'), ('MISS', 'Miss'), ('MS', 'Ms'), ('DR', 'Dr')], default=counsellor.enums.Honorifics['MR'], max_length=15, verbose_name='Title'),
        ),
    ]
