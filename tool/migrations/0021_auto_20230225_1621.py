# Generated by Django 3.2.10 on 2023-02-25 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0020_remove_ticket_on_hold'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nidanticket',
            name='callstart',
        ),
        migrations.AddField(
            model_name='nidanticket',
            name='remark',
            field=models.TextField(blank=True, null=True),
        ),
    ]
