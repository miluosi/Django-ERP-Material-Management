# Generated by Django 4.0.5 on 2022-08-17 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MM', '0013_alter_vendor_companycode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='companyCode',
            field=models.CharField(max_length=4),
        ),
    ]
