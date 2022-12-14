# Generated by Django 4.1.4 on 2022-12-26 10:37

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auctions', '0010_comment_unique_user_item_comment'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='comment',
            name='unique_user_item_comment',
        ),
        migrations.AlterUniqueTogether(
            name='comment',
            unique_together={('owner', 'item')},
        ),
    ]
