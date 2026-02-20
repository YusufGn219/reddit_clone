from django import forms
from django.core.exceptions import ValidationError

from .models import Community
from .utils import normalize_community_name

class CommunityCreateForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = ["name", "title", "description"]
    
    def clean_name(self):
        raw = self.cleaned_data.get("name","")
        name= normalize_community_name(raw)

        if len(name) < 3:
            raise ValidationError("Topluluk adı en az 3 karakter olmalı.")

        if len(name)>30:
            raise ValidationError("Topluluk adı en fazla 30 karakter olmalı.")
        
        if not name: 
            raise ValidationError("Topluluk adı boş olamaz.")
        
        if Community.objects.filter(name=name).exists():
            raise ValidationError("Bu topluluk adı zaten kullanılıyor.")
        
        return name