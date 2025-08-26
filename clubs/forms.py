from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # Club + author are set in the view to prevent cross-club posting
        fields = ["title", "content"]
