# Generated by Django 4.1.4 on 2022-12-26 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_remove_comment_unique_user_item_comment_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='comment',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='comment',
            constraint=models.UniqueConstraint(fields=('owner', 'item'), name='unique_user_item_comment'),
        ),
    ]