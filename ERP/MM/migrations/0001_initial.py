# Generated by Django 4.0.5 on 2022-08-01 14:04

import MM.models
from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='EUser',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to=settings.AUTH_USER_MODEL)),
                ('uid', models.AutoField(primary_key=True, serialize=False)),
                ('sector', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=11, validators=[MM.models.EUser.validate_phone])),
                ('question1', models.CharField(max_length=50)),
                ('answer1', models.CharField(max_length=50)),
                ('question2', models.CharField(max_length=50)),
                ('answer2', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]