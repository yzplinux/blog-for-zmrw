from django.shortcuts import render,get_object_or_404
from .models import Post,Category,Tag
from django.contrib.auth.models import User
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify
import markdown,re
# Create your views here.

def index(request):
    post_list = Post.objects.all()
    return render(request, 'blog/index.html', context={'post_list': post_list})

def detail(request,pk):
    post = get_object_or_404(Post,pk=pk)
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        TocExtension(slugify=slugify),
    ])
    post.body = md.convert(post.body)
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>',md.toc,re.S)
    post.toc = m.group(1) if m is not None else ''

    return render(request,'blog/detail.html',context={'post':post})

def archive(request,year,month):
    post_list = Post.objects.filter(
        created_time__year = year,
        created_time__month = month,
    )
    return render(request,'blog/index.html',context={'post_list':post_list})

def category(request,pk):
    cate = get_object_or_404(Category,pk=pk)
    post_list = Post.objects.filter(
        category = cate
    )
    return render(request,'blog/index.html',context={'post_list':post_list})

def tag(request,pk):
    t = get_object_or_404(Tag,pk=pk)
    post_list = Post.objects.filter(
        tags = t
    )
    return render(request,'blog/index.html',context={'post_list':post_list})

def author(request,author):
    u = get_object_or_404(User,username=author)
    post_list = Post.objects.filter(
        author = u
    )
    return render(request,'blog/index.html',context={'post_list':post_list})
