# Generated by Django 5.1.2 on 2024-10-24 15:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_planning_api', '0004_rename_evnet_invitation_event'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, null=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='EventInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_invitations', models.IntegerField(default=0)),
                ('total_rsvps', models.IntegerField(default=0)),
                ('total_accepted_rsvps', models.IntegerField(default=0)),
                ('total_rejected_rsvps', models.IntegerField(default=0)),
                ('invitaion_accepted_rsvps', models.IntegerField(default=0)),
                ('invitation_rejected_rsvps', models.IntegerField(default=0)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event_planning_api.event')),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]