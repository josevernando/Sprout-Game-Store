# Generated by Django 4.0.4 on 2022-06-14 09:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_alter_profile_profile_pic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='customer',
        ),
        migrations.AddField(
            model_name='review',
            name='profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.profile'),
        ),
    ]
