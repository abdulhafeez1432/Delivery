# Generated by Django 2.2 on 2020-07-27 19:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_order_bike'),
    ]

    operations = [
        migrations.AlterField(
            model_name='processorder',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='app.Category'),
        ),
    ]
