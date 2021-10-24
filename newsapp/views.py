from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import sessions
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404, reverse,HttpResponse,HttpResponseRedirect
from .models import *
import hashlib 
from datetime import datetime,date
import re
from django.http import JsonResponse, request
from django.views.generic import ListView,View
from django.contrib import messages


def cate():
    news={'n':'NEWS','w':'news'}
    sports={'n':'SPORTS','w':'sports'}
    tech={'n':'TECHNOLOGY','w':'tech'}
    business={'n':'BUSINESS','w':'business'}
    cinema={'n':'CINEMA','w':'cinema'}
    health={'n':'HEALTH','w':'health'}
    cat=[news,sports,tech,business,cinema,health]
    return cat

def home(request):
    context={}
    context['page_title'] = 'NEWSAVENUE'
    posts = Post.objects.all().order_by('-post_date')
    context['posts']=posts
    img = PostImage.objects.all()
    context['img']=img
    context['cat']=cate()
    check=register_table.objects.filter(user__id=request.user.id)
    if len(check)>0:
        reg=register_table.objects.get(user__id=request.user.id)
        context['reg']=reg
    return render(request,'blog/base.html',context)

def category(request,cat):
    context={}
    context['page_title'] = str(cat).upper()+' - NEWSAVENUE'
    posts = Post.objects.filter(category=cat).order_by('-post_date')
    context['posts']=posts
    img = PostImage.objects.all()
    context['img']=img
    context['cat']=cate()
    check=register_table.objects.filter(user__id=request.user.id)
    if len(check)>0:
        reg=register_table.objects.get(user__id=request.user.id)
        context['reg']=reg
    return render(request,'blog/base.html',context)

def search(request):
    context = {}
    sea = request.GET['b'] 
    sea = str(sea)
    if sea=='':
        return redirect('/')
    else:
        rejec = ['','a','an','the','is','are','or','and','can','could','may','might','then','if','this','that','these','those','it','he','she','to','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','as','you','of','in','has','will','we','by','us','our','its''your','all','for','on','at','his']
        sea_split = re.findall(r'[a-z0-9]*',sea.lower())
        while '' in sea_split:
            sea_split.remove('')
        print(sea_split)
        posts=Post.objects.all()
        post_sec = []
        for post in posts:
            post_tit_spl = re.findall(r'[a-z0-9]*',post.post_title.lower())
            post_desc_spl = re.findall(r'[a-z0-9]*',post.desc.lower())
            post_cate_spl = re.findall(r'[a-z0-9]*',post.category.lower())
            all_post_words = post_tit_spl + post_desc_spl + post_cate_spl
            post_tit_spl = []
            for w in all_post_words:
                if w not in rejec:
                    post_tit_spl.append(w)
            while('' in post_tit_spl):
                post_tit_spl.remove('')
            print('post_tit_spl',post_tit_spl)
            for spl in sea_split:
                print(spl)
                for post_tit in post_tit_spl:
                    reg = re.findall(spl,post_tit)
                    if len(reg)>0:
                        print('reg',reg)
                        while('' in reg):
                            reg.remove('')
                        post_sec.append(post)
                    reg = re.findall(post_tit,spl)
                    if len(reg)>0:
                        print('reg',reg)
                        while('' in reg):
                            reg.remove('')
                        post_sec.append(post)
                
                reg = re.findall(spl,post.category)
                if len(reg)>0:
                    print('reg',reg)
                    while('' in reg):
                        reg.remove('')
                    post_sec.append(post)
                reg = re.findall(post.category,spl)
                if len(reg)>0:
                    print('reg',reg)
                    while('' in reg):
                        reg.remove('')
                    post_sec.append(post)
                    
        post_cou = {}
        for post in post_sec:
            k = post_sec.count(post)
            post_cou[post.id] = k
        post_cou = sorted(post_cou.items(),key=lambda kv: kv[1],reverse=True)
        print(post_cou)
        post_fin = []
        for post in post_cou:
            post_fin.append(Post.objects.get(id=post[0]))
        context['posts'] = post_fin
    context['page_title'] = sea
    context['sea'] = sea
    context['cat']=cate()
    check=register_table.objects.filter(user__id=request.user.id)
    if len(check)>0:
        reg=register_table.objects.get(user__id=request.user.id)
        context['reg']=reg
    return render(request,'blog/base.html',context)

def news(request,sha):
    context={}
    check=Post.objects.filter(sha=sha)
    if len(check)>0:
        post=Post.objects.get(sha=sha)
        context['post']=post
        comments=Comment.objects.filter(post=post).order_by('-created')
        context['comments']=comments
        context['page_title'] = post.post_title + ' - NEWSAVENUE'
        context['cat']=cate()
        check=register_table.objects.filter(user__id=request.user.id)
        if len(check)>0:
            reg=register_table.objects.get(user__id=request.user.id)
            context['reg']=reg
        return render(request,'blog/news_open.html',context)

class comment(View):
    def get(self,request):
        comm = request.GET.get('comm',None)
        id=request.GET.get('id',None)
        data={}
        post = Post.objects.get(id=id)
        if register_table.objects.filter(user=request.user).exists():    
            user=request.user
            upload=Comment(user=user,post=post,desc=comm)
            upload.save()
            data['desc']=comm
            now=datetime.now()
            today = date.today()
            hou=now.hour
            am='a.m.'
            if hou>12:
                hou-=12
                am='p.m.'
            data['created']=today.strftime("%b. %d, %Y")+', '+str(hou)+now.strftime(":%M")+' '+am
            data['user']=user.username
        print(data)
        return JsonResponse(data)

class like(View):
    def get(self,request):
        id = request.GET.get('id',None)
        data={}
        post = Post.objects.get(id=id)
        if register_table.objects.filter(user=request.user).exists():
            if request.user in post.likes.all():
                post.likes.remove(request.user)
                data['like'] = False
            else:
                post.likes.add(request.user)
                data['like'] = True
            data['likecount'] = post.num_likes()
        print(data)
        return JsonResponse(data)

def openedit(request,sha):
    context={}
    check=Post.objects.filter(sha=sha)
    if len(check)>0:
        post=Post.objects.get(sha=sha)
        context['post']=post
        comments=Comment.objects.filter(post=post).order_by('-created')
        context['comments']=comments
        context['page_title'] = post.post_title + 'NEWSAVENUE'
        context['cat']=cate()
        check=register_table.objects.filter(user__id=request.user.id)
        if len(check)>0:
            reg=register_table.objects.get(user__id=request.user.id)
            context['reg']=reg
        context['page_title'] = 'EDIT' + str(post.post_title)
        context['cat']=cate()
    return render(request,'blog/openedit.html',context)

def dele(request,id):
    Post.objects.get(id=id).delete()
    return redirect('/')

def editsubmit(request,sha):
    context={}
    if request.method=="POST":
        id =request.POST['id']
        post = Post.objects.get(id=id)
        post.post_title = request.POST['title']
        post.category = request.POST['cate']
        post.place = request.POST['location']
        post.desc=request.POST['desc']
        if "newsimage" in request.FILES:
            post.cover = request.FILES["newsimage"]
        post.save()
    check=register_table.objects.filter(user__id=request.user.id)
    if len(check)>0:
        reg=register_table.objects.get(user__id=request.user.id)
        context['reg']=reg
    context['page_title'] = post.post_title + ' - NEWSAVENUE'
    context['cat']=cate()
    return redirect('/news/'+str(post.sha))

def addnews(request):
    context={}
    context['page_title']='Upload News'
    posts = Post.objects.all().order_by('-post_date')
    context['posts']=posts
    img = PostImage.objects.all()
    context['img']=img
    context['cat']=cate()
    check=register_table.objects.filter(user__id=request.user.id)
    if len(check)>0:
        reg=register_table.objects.get(user__id=request.user.id)
        context['reg']=reg
    return render(request,'blog/news_upload.html',context)

def uploadnews(request):
    if request.method=='POST':
        cate=request.POST['cate']
        place=None
        if "location" in request.POST:
            place=request.POST['location']
        title=request.POST['title']
        desc=request.POST['desc']
        user=request.user
        print('image')
        image = request.FILES["newsimage"]
        print(image)
        print('image uploaded')
        upload=Post(uname=user,post_title=title,desc=desc,category=cate,place=place,cover=image)
        upload.save()
        upload.sha = hashlib.sha1(str(upload.id).encode()).hexdigest()
        upload.save()
    return redirect('/addnews/')

'''
def comments(request,id):
    if request.method=='POST':
        desc=request.POST['desc']
        user=request.user
        post=Post.objects.get(id=id)
        upload=Comment(user=user,post=post,desc=desc)
        upload.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

'''

def sign_up(request):
    print('signup')
    if request.method=="POST":
        firstname = request.POST['firstname']
        lastname=None
        if "lastname" in request.POST:
            lastname = request.POST['lastname']
        email = request.POST['email']
        un = request.POST["username"]
        pwd = request.POST["password"]
        conpwd = request.POST['confirm-password']
        if pwd==conpwd:
            if User.objects.filter(username=un).exists():
                messages.success(request, 'Username already exists')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            elif User.objects.filter(email=email).exists():
                messages.success(request, 'Email already exists')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                user = User.objects.create_user(username = un, password = pwd, email = email,first_name = firstname, last_name = lastname)
                user.save()
                reg = register_table(firstname=firstname,lastname=lastname,email=email,user=user)
                reg.save()
                user = authenticate(username=un,password=pwd)
                if user:
                    login(request,user)
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                        #return redirect('/post/'+loc)
        else:
            messages.success(request, 'Confirm Password not matched')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def log_in(request):
    print('login')
    if request.method=="POST":
        un = request.POST["username"]
        pwd = request.POST["password"]
        check=User.objects.filter(username=un)
        if len(check)>0:
            user = authenticate(username=un,password=pwd)
            auth.login(request,user)
            if request.POST.get('rememberme', None):
                request.session['usern'] = un
                request.session['pwd'] = pwd
                print('sessions')
            else:
                request.session.set_expiry(0)
                print('sessions out')
        else:
            check=User.objects.filter(email=un)
            if len(check)>0:
                un=User.objects.get(email=un).username
                user = authenticate(username=un,password=pwd)
                auth.login(request,user)
                if request.POST.get('rememberme', None):
                    request.session['usern'] = un
                    request.session['pwd'] = pwd
                    print('sessions')
                else:
                    request.session.set_expiry(0)
                    print('sessions out')
            else:
                messages.success(request, 'Email not found')
        #if 'next' in request.POST:
         #   return redirect(request.POST['next'])
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def log_out(request):
    auth.logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))