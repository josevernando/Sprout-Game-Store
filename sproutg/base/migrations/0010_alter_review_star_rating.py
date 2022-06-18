# Generated by Django 4.0.4 on 2022-06-18 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_review_star_rating_approval'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='star_rating',
            field=models.CharField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=3, max_length=1),
        ),
    ]
