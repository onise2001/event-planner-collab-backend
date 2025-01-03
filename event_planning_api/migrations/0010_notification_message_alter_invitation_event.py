# Generated by Django 5.1.2 on 2024-11-01 15:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_planning_api', '0009_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='message',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='invitation',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invitations', to='event_planning_api.event'),
        ),
    ]
