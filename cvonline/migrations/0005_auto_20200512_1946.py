# Generated by Django 3.0.6 on 2020-05-12 11:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cvonline', '0004_auto_20200512_1943'),
    ]

    operations = [
        migrations.RenameField(
            model_name='donation',
            old_name='attn_from',
            new_name='attendee_from',
        ),
    ]
