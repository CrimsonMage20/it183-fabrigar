from django import forms
from .models import Food, Rating
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter username'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Enter password'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirm password'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].help_text = ''  # Removes help text

class EditFoodForm(forms.ModelForm):
    CATEGORY_CHOICES = [
        ('Almusal', 'Almusal'),
        ('Tanghalian', 'Tanghalian'),
        ('Hapunan', 'Hapunan'),
        ('Meryenda', 'Meryenda'),
    ]

    category = forms.ChoiceField(choices=CATEGORY_CHOICES, widget=forms.Select)

    class Meta:
        model = Food
        fields = ['name', 'description', 'image', 'category']

class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ['name', 'description', 'image']

class RatingForm(forms.ModelForm):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]  

    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.Select)

    class Meta:
        model = Rating
        fields = ['rating', 'comment']

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if int(rating) < 1 or int(rating) > 5:
            raise forms.ValidationError("Rating must be between 1 and 5.")
        return rating

