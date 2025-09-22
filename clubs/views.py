from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Club, Post

def user_can_manage_club(user, club: Club) -> bool:
    return user.is_authenticated and (user.is_superuser or club.coordinator_id == user.id)

def club_list(request):
    clubs = Club.objects.all().select_related("coordinator")
    return render(request, "clubs/club_list.html", {"clubs": clubs})

def club_detail(request, slug):
    club = get_object_or_404(Club.objects.select_related("coordinator"), slug=slug)
    posts = club.posts.select_related("author")
    can_add = user_can_manage_club(request.user, club)
    return render(request, "clubs/club_detail.html", {"club": club, "posts": posts, "can_add": can_add})

@login_required
def add_post(request, slug):
    club = get_object_or_404(Club, slug=slug)
    if not user_can_manage_club(request.user, club):
        messages.error(request, "You don't have permission to add posts for this club.")
        return redirect(club.get_absolute_url())

    if request.method == "POST":
        form = PostForm(request.POST, club=club, user=request.user)
        if form.is_valid():
            post = form.save(commit=False)
            post.club = club
            post.author = request.user
            post.save()
            messages.success(request, "Post created.")
            return redirect(club.get_absolute_url())
    else:
        form = PostForm(club=club, user=request.user)

    return render(request, "clubs/add_post.html", {"club": club, "form": form})

@login_required
def edit_post(request, slug, pk):
    club = get_object_or_404(Club, slug=slug)
    post = get_object_or_404(Post.objects.select_related("club"), pk=pk, club=club)
    if not user_can_manage_club(request.user, club):
        messages.error(request, "You don't have permission to edit posts for this club.")
        return redirect(club.get_absolute_url())

    if request.method == "POST":
        form = PostForm(request.POST, instance=post, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated.")
            return redirect(club.get_absolute_url())
    else:
        form = PostForm(instance=post, user=request.user)

    return render(request, "clubs/edit_post.html", {"club": club, "form": form, "post": post})

@login_required
def delete_post(request, slug, pk):
    club = get_object_or_404(Club, slug=slug)
    post = get_object_or_404(Post, pk=pk, club=club)
    if not user_can_manage_club(request.user, club):
        messages.error(request, "You don't have permission to delete posts for this club.")
        return redirect(club.get_absolute_url())

    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted.")
        return redirect(club.get_absolute_url())

    return render(request, "clubs/delete_post_confirm.html", {"club": club, "post": post})