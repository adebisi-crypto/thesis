from django import forms
from core.models import UserProfile, HealthData
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from core.models import BlogPost
from core.models import EducationalResource

User = get_user_model()

ETHNICITY_CHOICES = [
    ('white', 'White'),
    ('black_african', 'Black African'),
    ('black_caribbean', 'Black Caribbean'),
    ('indian', 'Indian'),
    ('pakistani', 'Pakistani'),
    ('bangladeshi', 'Bangladeshi'),
    ('other', 'Other'),
]

class UserProfileForm(forms.ModelForm):
    ethnicity = forms.ChoiceField(choices=ETHNICITY_CHOICES)
    class Meta:
        model = UserProfile
        fields = ['age', 'sex', 'ethnicity', 'smoker', 'diabetes']

class HealthDataForm(forms.ModelForm):
    class Meta:
        model = HealthData
        fields = ['systolic_bp', 'diastolic_bp', 'cholesterol_ratio', 'bmi', 'heart_rate']

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content']


class EducationalResourceForm(forms.ModelForm):
    class Meta:
        model = EducationalResource
        fields = ['title', 'description', 'url', 'category']

