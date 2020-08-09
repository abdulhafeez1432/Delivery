# Generated by Django 2.2 on 2020-08-06 08:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_remove_processorder_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='processorder',
            name='subcategory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcategory', to='app.SubCategory'),
        ),
    ]
