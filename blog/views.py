
from django.core import paginator
from django.db.models import Count
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response, get_object_or_404
from django.conf import settings


# Create your views here.
from blog.models import Blog,BlogType
from read_statistics.utils import read_statistics_once_read
def blog_list_common_date(request,blogs_list):
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    p = Paginator(blogs_list,settings.EACH_PAGE_BLOGS,request=request)
    page_list = p.page(page)

    blog_dates = Blog.objects.dates('created_time', 'month', order='DESC')
    blog_dates_dict = {}

    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year,created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count

    context = {}
    context['blogs'] = page_list.object_list
    context['page_list'] = page_list
    context['blogs_type'] = BlogType.objects.annotate(blog_count=Count('blog'))
    context['blog_dates'] = blog_dates_dict
    return context

def blog_list(request):
    blogs_list = Blog.objects.all()
    # 使用paginator设置分页
    # paginator = Paginator(blogs_list,2)                # 每10条进行分页
    # page_num = request.GET.get('page', 1)               # 获取URL的页码参数(GET请求)
    # page_of_blogs = paginator.get_page(page_num)
    # current_page_num = page_of_blogs.number                     #获取当前页码
    # page_range = [x for x in range(current_page_num-2,current_page_num+3) if 0 < x < paginator.num_pages]

    # 使用pure_pagination设置分页
    context = blog_list_common_date(request,blogs_list)
    context['blogs_list'] = blogs_list
    return render_to_response('blog/blog_list.html',context)

def blog_with_type(request,blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blogs_list = Blog.objects.filter(blog_type=blog_type)
    context = blog_list_common_date(request, blogs_list)
    context['blog_type'] = blog_type
    return render_to_response('blog/blog_with_type.html',context)

def blog_with_date(request,year,month):
    blogs_list = Blog.objects.filter(created_time__year=year,created_time__month=month)
    context = blog_list_common_date(request, blogs_list)
    context['blog_with_date'] = '%s年%s月'%(year,month)
    return render_to_response('blog/blog_with_date.html', context)

def blog_detail(request,blog_pk):
    blog = get_object_or_404(Blog,pk=blog_pk)
    blogs_list = Blog.objects.all()
    read_cookie_key = read_statistics_once_read(request,blog)
    context = blog_list_common_date(request,blogs_list)
    context['blog'] = blog
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    response = render_to_response('blog/blog_detail.html',context)                  # 响应
    response.set_cookie(read_cookie_key,'true')                                     # 阅读cookie标记
    return response




