# Generated by Django 4.1.2 on 2022-10-28 13:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import encrypted_model_fields.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='NotionAuthorization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_token', encrypted_model_fields.fields.EncryptedCharField()),
                ('bot_id', models.CharField(max_length=100)),
                ('duplicated_template_id', models.CharField(blank=True, max_length=100, null=True)),
                ('workspace_name', models.CharField(max_length=500)),
                ('workspace_icon', models.URLField()),
                ('workspace_id', models.CharField(max_length=100)),
                ('owner', models.JSONField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
