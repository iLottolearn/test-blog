from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
    list_display = ('read_num','content_type')

@admin.register(models.ReadDetail)
class ReadNumAdmin(admin.ModelAdmin):
    list_display = ('date','read_num','content_object')