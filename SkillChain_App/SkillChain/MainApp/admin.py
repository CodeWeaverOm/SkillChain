from django.contrib import admin
from .models import Profile, Skill, Video, Rating, Education, Experience, Certificate, Expert, Competition
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User



admin.site.register(Profile)
admin.site.register(Skill)
admin.site.register(Video)
admin.site.register(Rating)
admin.site.register(Education)
admin.site.register(Experience)
admin.site.register(Certificate)

# Expert system models
admin.site.register(Expert)
admin.site.register(Competition)