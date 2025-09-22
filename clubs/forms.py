# forms.py
from django import forms
from django.core.exceptions import ValidationError
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]  # author/club set in the view

    def __init__(self, *args, **kwargs):
        # Expect the view to pass club and user so we can validate
        self.club = kwargs.pop("club", None)
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned = super().clean()
        # When editing, prefer instance.club over passed club
        club = self.instance.club if self.instance and self.instance.pk else self.club
        user = self.user
        if not club or not user:
            raise ValidationError("Missing context to validate permissions.")
        if club.coordinator_id != user.id and not getattr(user, "is_superuser", False):
            raise ValidationError("Only the club coordinator can manage posts for this club.")
        return cleaned
