from django.contrib import admin
from .models import CustomUser, Log, FindIndex

admin.site.register(CustomUser)

@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'sub_type', 'shift_name', 'description', 'date', 'created_by']

@admin.register(FindIndex)
class FindIndexAdmin(admin.ModelAdmin):
    list_display = ['id', 'log_data', 'user']