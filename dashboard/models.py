from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    branch = models.CharField(max_length=100)
    year = models.CharField(max_length=10)
    college = models.CharField(max_length=200)

    def __str__(self):
        return self.user.username

class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', default='default.jpg')
    skills = models.ManyToManyField(Skill, blank=True)

    def __str__(self):
        return self.user.username

class SkillPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    is_teaching = models.BooleanField(default=True)  # True = teaching, False = learning
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"
    


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField()
    link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"


class Message(models.Model):
    sender = models.ForeignKey(User, related_name="sent_messages", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="received_messages", on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender} to {self.receiver}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.message}"

class Connection(models.Model):
    from_user = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("from_user", "to_user")

    def __str__(self):
        return f"{self.from_user.username} -> {self.to_user.username}"


class Endorsement(models.Model):
    skill = models.ForeignKey(SkillPost, related_name="endorsements", on_delete=models.CASCADE)
    endorsed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("skill", "endorsed_by")

    def __str__(self):
        return f"{self.endorsed_by.username} endorsed {self.skill.title}"