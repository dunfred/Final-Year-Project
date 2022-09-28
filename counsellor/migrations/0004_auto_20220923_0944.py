# Generated by Django 3.1.4 on 2022-09-23 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('counsellor', '0003_auto_20220923_0919'),
    ]

    operations = [
        migrations.CreateModel(
            name='CounsellingType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(max_length=100, verbose_name='Type')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='counsellor',
            name='fields',
            field=models.ManyToManyField(blank=True, related_name='counsellors', to='counsellor.CounsellingType'),
        ),
    ]