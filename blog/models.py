from django.contrib.auth.models import User
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models.fields import exceptions
from django.utils import timezone
from read_statistics.models import ReadNumExpandMethod
# Create your models here.



class BlogType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name


class Blog(models.Model,ReadNumExpandMethod):
    title = models.CharField(max_length=50)
    blog_type = models.ForeignKey(BlogType,on_delete=models.DO_NOTHING)
    content = RichTextUploadingField()
    author = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(default=timezone.now)
    last_updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '<Blog:%s>'%self.title

    class Meta:
        ordering = ['-created_time']




