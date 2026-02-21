from django import forms
from .models import Post, Comment

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["community", "title", "body"]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]

    def clean_body(self):
        body = (self.cleaned_data.get("body")or"").strip()
        if len(body)<2:
            raise forms.ValidationError("Yorum çok kısa.")
        return body