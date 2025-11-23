from django import forms
from .models import Profile, Education, Experience, Certificate, Video

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "image",
            "tagline",
            "summary",
            "linkedin",
            "github",
            "website",
            "level",
            "xp",
            "status",
        ]
        widgets = {
            "tagline": forms.TextInput(attrs={"class": "w-full p-2 border rounded"}),
            "summary": forms.Textarea(attrs={"class": "w-full p-2 border rounded", "rows": 4}),
            "linkedin": forms.URLInput(attrs={"class": "w-full p-2 border rounded"}),
            "github": forms.URLInput(attrs={"class": "w-full p-2 border rounded"}),
            "website": forms.URLInput(attrs={"class": "w-full p-2 border rounded"}),
            "level": forms.NumberInput(attrs={"class": "w-full p-2 border rounded"}),
            "xp": forms.NumberInput(attrs={"class": "w-full p-2 border rounded"}),
            "status": forms.TextInput(attrs={"class": "w-full p-2 border rounded"}),
        }

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ["degree", "institute", "year"]
        widgets = {
            "degree": forms.TextInput(attrs={"class": "w-full p-2 border rounded"}),
            "institute": forms.TextInput(attrs={"class": "w-full p-2 border rounded"}),
            "year": forms.TextInput(attrs={"class": "w-full p-2 border rounded"}),
        }

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ["company", "role", "duration", "description"]
        widgets = {
            "company": forms.TextInput(attrs={"class": "w-full p-2 border rounded"}),
            "role": forms.TextInput(attrs={"class": "w-full p-2 border rounded"}),
            "duration": forms.TextInput(attrs={"class": "w-full p-2 border rounded"}),
            "description": forms.Textarea(attrs={"class": "w-full p-2 border rounded", "rows": 3}),
        }

class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ["title", "certificate_file", "date"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "w-full p-2 border rounded"}),
            "date": forms.DateInput(attrs={"class": "w-full p-2 border rounded", "type": "date"}),
        }

class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ["title", "video_file", "thumbnail", "skills"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "w-full p-2 border rounded"}),
        }
