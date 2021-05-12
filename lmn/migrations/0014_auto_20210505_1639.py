# Generated by Django 3.1.7 on 2021-05-05 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lmn', '0013_showrating_user'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='showrating',
            constraint=models.UniqueConstraint(fields=('show', 'user'), name='user_rated_show'),
        ),
    ]
