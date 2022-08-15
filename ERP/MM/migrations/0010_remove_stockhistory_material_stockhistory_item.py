# Generated by Django 4.0.5 on 2022-08-15 05:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MM', '0009_material_euser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stockhistory',
            name='material',
        ),
        migrations.AddField(
            model_name='stockhistory',
            name='item',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='MM.materialitem'),
            preserve_default=False,
        ),
    ]
