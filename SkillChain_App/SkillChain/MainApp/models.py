from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# -------------------- SKILL --------------------

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# -------------------- PROFILE --------------------

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, blank=True)  # ADD THIS
    skills = models.ManyToManyField(Skill, blank=True)
    image = models.ImageField(upload_to="profiles/", default="default.png")

    tagline = models.CharField(max_length=200, blank=True)
    summary = models.TextField(blank=True)

    linkedin = models.CharField(max_length=400, blank=True)
    github = models.CharField(max_length=400, blank=True)
    website = models.CharField(max_length=400, blank=True)

    level = models.IntegerField(default=1)
    xp = models.IntegerField(default=0)
    status = models.CharField(max_length=50, default="Beginner")
    def add_xp(self, amount):
        self.xp += amount

        # Auto-level up every 100 XP
        while self.xp >= self.level * 100:
            self.level += 1

        self.save()

# -------------------- VIDEO --------------------

class Video(models.Model):
    uploader = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="videos")
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to="videos/")
    thumbnail = models.URLField(blank=True, null=True)
    skills = models.ManyToManyField(Skill, blank=True, related_name="videos")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


# -------------------- RATING --------------------

class Rating(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="ratings")
    rated_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="given_ratings")
    stars = models.IntegerField()  # 1–5
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        pass


    def __str__(self):
        return f"{self.rated_by} → {self.video}: {self.stars}"


# -------------------- EDUCATION --------------------

class Education(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="educations")
    degree = models.CharField(max_length=100)
    institute = models.CharField(max_length=200)
    year = models.CharField(max_length=10)

    def __str__(self):
        return self.degree


# -------------------- EXPERIENCE --------------------

class Experience(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="experiences")
    company = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    duration = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.company


# -------------------- CERTIFICATE --------------------

class Certificate(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="certificates")
    title = models.CharField(max_length=200)
    certificate_file = models.FileField(upload_to="certificates/")
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title
    
# -------------------- Peer --------------------

class Peer(models.Model):
    from_user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="sent_peers")
    to_user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="received_peers")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f"{self.from_user.user.username} → {self.to_user.user.username}"
    

# -----------------------------Expert -------------------------------------------
class Expert(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    skills = models.ManyToManyField(Skill)

    def __str__(self):
        return self.user.username


class Competition(models.Model):
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to="competition_images/")
    
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    skills = models.ManyToManyField(Skill)

    created_at = models.DateTimeField(auto_now_add=True)

    def is_live(self):
        from django.utils import timezone
        now = timezone.now()
        return self.start_date <= now <= self.end_date

    def is_closed(self):
        from django.utils import timezone
        now = timezone.now()
        return now > self.end_date

    def __str__(self):
        return self.title


class CompetitionParticipation(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    participated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.user.username} → {self.competition.title}"

