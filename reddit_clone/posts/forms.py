from django import forms
from .models import Post, Comment

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["community", "title", "post_type","body", "image", "url"]
        widgets = {
            "post_type": forms.RadioSelect,
            "body": forms.Textarea(attrs={"rows": 8, "placeholder": "Metin..."}),
            "url": forms.TextInput(attrs={"placeholder": "https://github.com/yusufgn219", "style": "width:100%;"}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]

    def clean_body(self):
        body = (self.cleaned_data.get("body")or"").strip()
        if len(body)<2:
            raise forms.ValidationError("Yorum çok kısa.")
        return body


class PostEditForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=['title','body','url']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'url': forms.TextInput(attrs={'class': 'form-control'}),
        }