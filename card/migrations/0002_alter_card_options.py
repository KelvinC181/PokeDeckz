# Generated by Django 4.2.17 on 2025-01-16 11:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='card',
            options={'ordering': ['card_id']},
        ),
    ]
