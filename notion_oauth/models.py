from django.db import models
from django.conf import settings

from encrypted_model_fields.fields import EncryptedCharField  

class NotionAuthorization(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    access_token = EncryptedCharField(max_length=100)
    bot_id = models.CharField(max_length=100) # Maybe Primary Key
    duplicated_template_id = models.CharField(max_length=100, blank=True, null=True)
    workspace_name = models.CharField(max_length=500)
    workspace_icon = models.URLField()
    workspace_id = models.CharField(max_length=100)
    owner = models.JSONField() # Don't really care about details for now but want to store

    def __str__(self):
        return self.workspace_name