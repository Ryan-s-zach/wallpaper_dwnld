# wallpapers/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Wallpaper, User, Category

class CustomUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class WallpaperForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Wallpaper
        fields = ['title', 'w_image', 'resolution_width', 'resolution_height', 'file_size', 'status', 'categories']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


