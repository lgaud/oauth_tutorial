from django.contrib import admin

from .models import NotionAuthorization

# Register your models here.
@admin.register(NotionAuthorization)
class NotionAuthorizationAdmin(admin.ModelAdmin):
    list_display = ['user', 'workspace_name', 'workspace_id']