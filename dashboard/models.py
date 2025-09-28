from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    branch = models.CharField(max_length=100)
    year = models.CharField(max_length=10)
    college = models.CharField(max_length=200)

    def __str__(self):
        return self.user.username

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    

class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username

class Club(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True,null = True)
    date = models.DateField()
    club = models.ForeignKey(Club,on_delete=models.CASCADE,related_name="events",blank=True,null=True)

    def __str__(self):
        return self.title

class Academic(models.Model):
    title = models.CharField(max_length=200)  
    code = models.CharField(max_length=50, unique=True)  
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.code} - {self.title}"

class Post(models.Model):
    author = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.author.user.username} on {self.created_at.date()}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="userprofile")
    bio = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(upload_to="profile_pics/", default="default.jpg")
    skills = models.ManyToManyField(Skill, blank=True, related_name="users")

    def _str_(self):
        return self.user.username

class SkillPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="skill_posts")
    title = models.CharField(max_length=200)
    description = models.TextField()
    is_teaching = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.user} - {self.title}"

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")
    title = models.CharField(max_length=150)
    description = models.TextField()
    link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.title} - {self.user}"

class Message(models.Model):
    sender = models.ForeignKey(User, related_name="sent_messages", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="received_messages", on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"From {self.sender} to {self.receiver}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    class Meta:
        ordering = ['-created_at']
    def _str_(self):
        return f"{self.user} - {self.message}"

class Connection(models.Model):
    from_user = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("from_user", "to_user")

    def _str_(self):
        return f"{self.from_user} -> {self.to_user}"

class Endorsement(models.Model):
    # keep name but clarify it's endorsing a SkillPost
    skill = models.ForeignKey(SkillPost, related_name="endorsements", on_delete=models.CASCADE)
    endorsed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="given_endorsements")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("skill", "endorsed_by")

    def _str_(self):
        return f"{self.endorsed_by} endorsed {self.skill.title}"