from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.urls import reverse

 
User = settings.AUTH_USER_MODEL

class Club(models.Model):
    name = models.CharField(max_length=100, unique = True)
    slug = models.SlugField(max_length=120, unique=True, help_text="Used un URLS (e.g. /clubs/gfg)")
    coordinator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank = True, 
        related_name='coordinated_clubs',
        help_text = "Each club can have one coordinator. Set by admin."
    )

    class Meta:
        ordering = ["name"]
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("clubs:club_detail", args = [self.slug])
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Post(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="club_posts")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} - ({self.club.name})"

    def get_edit_url(self):
        return reverse("clubs:edit_post", args=[self.club.slug, self.pk])
    
    def delete_url(self):
        return reverse("clubs:delete_post", args=[self.club.slug, self.pk])