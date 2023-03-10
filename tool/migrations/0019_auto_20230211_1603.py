# Generated by Django 3.2.10 on 2023-02-11 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0018_remove_nidanticket_street_test'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='nidanticket',
            options={'ordering': ['created_date']},
        ),
        migrations.AlterModelOptions(
            name='operator',
            options={'ordering': ['date_created']},
        ),
        migrations.AddIndex(
            model_name='nidanticket',
            index=models.Index(fields=['created_date'], name='tool_nidant_created_6b6507_idx'),
        ),
        migrations.AddIndex(
            model_name='operator',
            index=models.Index(fields=['date_created'], name='tool_operat_date_cr_5a1398_idx'),
        ),
    ]
