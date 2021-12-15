from django.conf import settings as conf_settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm, CommentForm
from .models import Group, Post, User, Follow

TITLE_DICT = conf_settings.TITLE_DICT
PAGE_COUNT = conf_settings.PAGINATOR_COUNT_PAGE


def index(request):
    title = TITLE_DICT.get('index')
    posts = Post.objects.all()
    paginator = Paginator(posts, PAGE_COUNT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj,
               'title': title
               }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    title = TITLE_DICT.get('group_posts')
    group = get_object_or_404(Group, slug=slug)
    posts = group.group.all()
    paginator = Paginator(posts, PAGE_COUNT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'group': group,
               'page_obj': page_obj,
               'title': title.format(group=group)
               }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):  # AnonymousUser
    title = TITLE_DICT.get('profile')
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user)
    paginator = Paginator(posts, PAGE_COUNT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    following = False
    if str(request.user) != 'AnonymousUser':
        following = Follow.objects.filter(user=request.user,
                                          author=user).exists()

    context = {'page_obj': page_obj,
               'title': title.format(user=user),
               'author': user,
               'following': following
               }

    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    form = CommentForm(request.POST or None)
    post = get_object_or_404(Post, pk=post_id)
    title = post.text[:30]
    comments = post.comments.all()
    context = {'post': post,
               'title': title,
               'form': form,
               'comments': comments
               }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    title = TITLE_DICT.get('post_create')
    form = PostForm(request.POST or None, files=request.FILES or None,)
    if request.method == 'POST' and form.is_valid():
        user = request.user
        post = form.save(commit=False)
        post.author = user
        post.save()
        return redirect('posts:profile', username=user)
    context = {'form': form,
               'title': title
               }

    return render(request, 'posts/post_create.html', context)


@login_required
def post_edit(request, post_id):
    title = TITLE_DICT.get('post_edit')
    post = Post.objects.get(pk=post_id)
    user = request.user
    form = PostForm(request.POST or None,
                    files=request.FILES or None,
                    instance=post
                    )
    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        post.author = user
        post.save()
        return redirect('posts:post_detail', post_id=post_id)
    if post.author == user:
        context = {'form': form,
                   'is_edit': True,
                   'title': title
                   }

        return render(request, 'posts/post_create.html', context)

    return redirect('posts:post_detail', post_id=post_id)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    user = request.user
    title = TITLE_DICT.get('index')
    follow = user.follower.all()
    authors = [i.author for i in follow]
    posts = Post.objects.filter(author__in=authors)
    paginator = Paginator(posts, PAGE_COUNT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj, 'title': title}
    return render(request, 'posts/follow.html', context)


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    user = request.user
    following = Follow.objects.filter(user=user, author=author).exists()
    if not following and user != author:
        Follow.objects.create(user=user, author=author)
    return redirect('posts:profile', username=username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    user = request.user
    following = Follow.objects.filter(user=user, author=author)
    following.delete()
    return redirect('posts:profile', username=username)
