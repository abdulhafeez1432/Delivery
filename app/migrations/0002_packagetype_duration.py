# Generated by Django 3.0.8 on 2020-07-23 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='packagetype',
            name='duration',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=5, verbose_name='Duration Time'),
            preserve_default=False,
        ),
    ]
