import datetime

from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum
from django.utils import timezone

from .models import ReadNum,ReadDetail

def read_statistics_once_read(request,obj):
    ct = ContentType.objects.get_for_model(obj)
    key = '%s_%s_read'%(ct.model,obj.pk)

    if not request.COOKIES.get(key):
        # 总阅读数+1
        readnum,created =ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
        # if ReadNum.objects.filter(content_type=ct,object_id=obj.pk).count():
        #     readnum = ReadNum.objects.get(content_type=ct,object_id=obj.pk)         #存在记录
        # else:
        #     readnum = ReadNum(content_type=ct,object_id=obj.pk)                     #不存在记录
        readnum.read_num +=1
        readnum.save()
        # 每日阅读数+1
        date = timezone.now().date()
        readDetail,created = ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.pk, date=date)
        # if ReadDetail.objects.filter(content_type=ct,object_id=obj.pk,date=date).count():
        #     readDetail = ReadDetail.objects.get(content_type=ct,object_id=obj.pk,date=date)         #存在记录
        # else:
        #     readDetail = ReadDetail(content_type=ct,object_id=obj.pk,date=date)                     #不存在记录
        readDetail.read_num +=1
        readDetail.save()
    return key

def get_seven_days_read_num(conttent_type):
    today = timezone.now().date()
    dates = []
    read_nums = []
    for i in range(7,0,-1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))
        read_details = ReadDetail.objects.filter(content_type=conttent_type,date=date)
        result = read_details.aggregate(read_num_sum = Sum('read_num'))
        read_nums.append(result['read_num_sum'] or 0)
    return read_nums,dates










