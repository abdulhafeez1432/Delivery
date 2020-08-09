# Generated by Django 3.0.8 on 2020-07-23 17:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20200723_1807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='package',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='package', to='app.PackageType'),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Food Name'),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Food Price'),
        ),
    ]