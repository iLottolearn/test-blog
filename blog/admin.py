from django.contrib import admin
from . import models
# Register your models here.
@admin.register(models.BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('id','type_name')

@admin.register(models.Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id','title','blog_type','author','get_read_num','created_time','last_updated_time')

