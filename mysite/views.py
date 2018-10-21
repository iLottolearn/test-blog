from blog.models import Blog
from django.shortcuts import render_to_response
from read_statistics.utils import get_seven_days_read_num
from django.contrib.contenttypes.models import ContentType

def home(request):
    conttent_type = ContentType.objects.get_for_model(Blog)
    read_nums,dates = get_seven_days_read_num(conttent_type)
    context = {}
    context['read_nums'] = read_nums
    context['dates'] = dates
    return render_to_response('home.html',context)
