# Generated by Django 4.0.4 on 2022-05-18 02:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_rename_reveiew_review'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Customer',
        ),
        migrations.DeleteModel(
            name='Developer',
        ),
        migrations.RemoveField(
            model_name='review',
            name='account',
        ),
        migrations.RemoveField(
            model_name='review',
            name='gameid',
        ),
        migrations.RemoveField(
            model_name='transaksi',
            name='customerid',
        ),
        migrations.DeleteModel(
            name='Game',
        ),
        migrations.DeleteModel(
            name='Review',
        ),
        migrations.DeleteModel(
            name='Transaksi',
        ),
    ]