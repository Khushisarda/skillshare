from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import RegisterForm, LoginForm
from .models import Profile
from .forms import UserProfileForm
from .models import UserProfile
from .models import SkillPost
from .models import Project
from .models import Notification,Connection, Endorsement,Message, Skill
from django.db.models import Q
from .models import Person, Skill, Club,Event,Academic,Post
from django.http import JsonResponse

def search(request):
    query = request.GET.get("q", "").strip()

    if not query:
        return render(request, "search/results.html", {"query": query})

    people = Person.objects.filter(Q(name__icontains=query) | Q(username__icontains=query))[:20]
    skills = Skill.objects.filter(name__icontains=query)[:20]
    clubs = Club.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))[:20]
    events = Event.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))[:20]
    academics = Academic.objects.filter(Q(title__icontains=query) | Q(code__icontains=query))[:20]
    posts = Post.objects.filter(content__icontains=query)[:20]

    return render(request, "search/results.html", {
        "query": query,
        "people": people,
        "skills": skills,
        "clubs": clubs,
        "events": events,
        "academics": academics,
        "posts": posts,
    })



def home(request):
    return render(request, 'dashboard/index.html')

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Save profile
            Profile.objects.create(
                user=user,
                branch=form.cleaned_data["branch"],
                year=form.cleaned_data["year"],
                college=form.cleaned_data["college"]
            )
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "dashboard/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard")
    else:
        form = LoginForm()
    return render(request, "dashboard/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # redirect to profile page after saving
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'dashboard/profile.html', {'form': form, 'profile': profile})


@login_required
def dashboard(request):
    profile = UserProfile.objects.get_or_create(user=request.user)[0]
    skills = SkillPost.objects.filter(user=request.user)
    projects = Project.objects.filter(user=request.user)
    notifications = Notification.objects.filter(user=request.user, is_read=False)

    return render(request, "dashboard/dashboard.html", {
        "profile": profile,
        "skills": skills,
        "projects": projects,
        "notifications": notifications,
    })


@login_required
def edit_profile(request):
    profile = UserProfile.objects.get_or_create(user=request.user)[0]
    if request.method == "POST":
        bio = request.POST.get("bio")
        profile.bio = bio
        if "profile_pic" in request.FILES:
            profile.profile_pic = request.FILES["profile_pic"]
        profile.save()
        return redirect("dashboard")
    return render(request, "dashboard/edit_profile.html", {"profile": profile})


@login_required
def add_project(request):
    """used to add new project in user dashboard"""
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        link = request.POST.get("link")
        Project.objects.create(user=request.user, title=title, description=description, link=link)
        Notification.objects.create(user=request.user, message="New project added!")
        return redirect("dashboard")
    return render(request, "dashboard/add_project.html")

@login_required
def add_skill(request):
    if request.method == "POST":
        name = request.POST.get("name")
        Skill.objects.create(user=request.user,name=name)
        Notification.objects.create(user=request.user,message="new skill added!")
        return redirect("dashboard")
    return render(request, "dashboard/add_skill.html")
    

@login_required
def send_message(request, user_id):
    receiver = User.objects.get(id=user_id)
    if request.method == "POST":
        content = request.POST.get("content")
        Message.objects.create(sender=request.user, receiver=receiver, content=content)
        Notification.objects.create(user=receiver, message=f"New message from {request.user.username}")
        return redirect("dashboard")
    return render(request, "dashboard/send_message.html", {"receiver": receiver})

@login_required
def notifications_page(request):
    return render(request, "dashboard/notifications.html")


@login_required
def notifications_api(request):
    notifications = Notification.objects.filter(user=request.user)
    data = [
        {
            'id' : n.id,
            'message': n.message,
            'read': n.read,
            'timestamp': n.created_at.isoformat()
        } for n in notifications
    ]
    return JsonResponse(data, safe=False)

@login_required
def mark_notification_read(request, notif_id):

    # Mark notification as read
    try:
        n = Notification.objects.get(id=notif_id, user=request.user)
        n.read = True
        n.save()
        return JsonResponse({'status': 'success'})
    except Notification.DoesNotExist:
        return JsonResponse({'status': 'error'}, status=404)
@login_required
def dashboard_home(request):
    unread_count = Notification.objects.filter(user=request.user, read=False).count()
    return render(request, "dashboard/home.html", {"unread_count": unread_count})
        

@login_required
def follow_user(request, user_id):
    to_user = get_object_or_404(User, id=user_id)
    if request.user != to_user:
        Connection.objects.get_or_create(from_user=request.user, to_user=to_user)
    return redirect("dashboard")

@login_required
def unfollow_user(request, user_id):
    Connection.objects.filter(from_user=request.user, to_user_id=user_id).delete()
    return redirect("dashboard")


# --- Feed ---
@login_required
def feed(request):
    following = Connection.objects.filter(from_user=request.user).values_list("to_user", flat=True)
    posts = SkillPost.objects.filter(user__in=following).order_by("-created_at")
    return render(request, "dashboard/feed.html", {"posts": posts})


# --- Search ---
@login_required
def search(request):
    query = request.GET.get("q", "")
    users = User.objects.filter(username__icontains=query) if query else []
    skills = SkillPost.objects.filter(title__icontains=query) if query else []
    return render(request, "dashboard/search.html", {"users": users, "skills": skills, "query": query})


# --- Endorsements ---
@login_required
def endorse_skill(request, skill_id):
    skill = get_object_or_404(SkillPost, id=skill_id)
    if request.user != skill.user:
        Endorsement.objects.get_or_create(skill=skill, endorsed_by=request.user)
    return redirect("dashboard")


# --- Settings ---
@login_required
def settings_page(request):
    profile = request.user.userprofile
    if request.method == "POST":
        profile.bio = request.POST.get("bio")
        profile.save()
    return render(request, "dashboard/settings.html", {"profile": profile})