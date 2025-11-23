from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from .forms import ProfileForm, EducationForm, ExperienceForm
from .models import Profile, Skill, Video, Rating, Education, Experience, Certificate, Peer, Competition, Expert, CompetitionParticipation
from django.utils import timezone

# -------------------- SIGNUP --------------------

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm')
        skill_name = request.POST.get('skill')  # single skill

        if password != confirm:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('signup')

        user = User.objects.create_user(username=username, password=password)
        profile = Profile.objects.create(user=user)

        # Save skill on signup
        if skill_name:
            skill_obj, created = Skill.objects.get_or_create(name=skill_name)
            profile.skills.add(skill_obj)

        messages.success(request, "Account created successfully!")
        return redirect('login')

    return render(request, 'MainApp/signup.html')


# -------------------- LOGIN --------------------

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')

        messages.error(request, "Invalid username or password")
        return redirect('login')

    return render(request, 'MainApp/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# -------------------- HOME --------------------

@login_required
def home(request):
    profile = request.user.profile
    user_skills = profile.skills.all()

    # Get videos uploaded by other users with overlapping skills
    suggested_videos = Video.objects.filter(
        skills__in=user_skills
    ).exclude(uploader=profile).distinct()

    # Optional: order by number of matching skills
    from django.db.models import Count
    suggested_videos = suggested_videos.annotate(
        matches=Count('skills')
    ).order_by('-matches', '-created_at')

    # Load current user's ratings
    user_ratings = {
        r.video.id: r.stars
        for r in Rating.objects.filter(rated_by=profile)
    }

    return render(request, "MainApp/home.html", {
        "profile": profile,
        "suggested_videos": suggested_videos,
        "user_ratings": user_ratings,
    })


# -------------------- RATE VIDEO --------------------

@login_required
def rate_video(request, video_id):
    if request.method == "POST":
        stars = int(request.POST.get("stars"))
        profile = request.user.profile
        video = get_object_or_404(Video, id=video_id)

        # Check if rating already exists
        existing = Rating.objects.filter(video=video, rated_by=profile).first()

        if existing:
            # update stars only → NO XP gained
            existing.stars = stars
            existing.save()
        else:
            # first rating → create + give XP
            Rating.objects.create(video=video, rated_by=profile, stars=stars)

            xp_to_add = stars * 10
            video.uploader.add_xp(xp_to_add)

        return JsonResponse({"success": True, "stars": stars})

    return JsonResponse({"success": False})



# -------------------- PROFILE PAGE --------------------

@login_required
def profile_page(request):
    profile = request.user.profile
    education = profile.educations.all()
    experience = profile.experiences.all()

    return render(request, "MainApp/profile.html", {
        "profile": profile,
        "education_list": education,
        "experience_list": experience,
        "profile_form": ProfileForm(instance=profile),
        "edu_form": EducationForm(),
        "exp_form": ExperienceForm(),
    })


# -------------------- SAVE PROFILE (FORM) --------------------

@login_required
def save_profile(request):
    profile = request.user.profile
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
    return redirect("profile")


# -------------------- ADD EDUCATION --------------------

@login_required
def add_education(request):
    profile = request.user.profile
    form = EducationForm(request.POST)
    if form.is_valid():
        new = form.save(commit=False)
        new.profile = profile
        new.save()
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"})


# -------------------- ADD EXPERIENCE --------------------

@login_required
def add_experience(request):
    profile = request.user.profile
    form = ExperienceForm(request.POST)
    if form.is_valid():
        new = form.save(commit=False)
        new.profile = profile
        new.save()
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"})


# -------------------- EDIT PROFILE --------------------
@login_required
def edit_profile(request):
    profile = request.user.profile

    if request.method == "POST":
        profile.tagline = request.POST.get("tagline")
        profile.summary = request.POST.get("summary")
        profile.linkedin = request.POST.get("linkedin")
        profile.github = request.POST.get("github")
        profile.website = request.POST.get("website")

        if request.FILES.get("image"):
            profile.image = request.FILES.get("image")

        profile.save()
        return JsonResponse({"success": True})

    return render(request, "MainApp/forms/edit_profile_form.html", {"profile": profile})




# -------------------- TAB LOADER --------------------

@login_required
def load_profile_tab(request, tab):
    profile = request.user.profile

    if tab == "profile":
        return render(request, "MainApp/profile_tabs/profile_tab.html", {
            "profile": profile,
            "educations": profile.educations.all(),
            "experiences": profile.experiences.all(),
        })

    if tab == "videos":
        return render(request, "MainApp/profile_tabs/videos_tab.html", {
            "videos": profile.videos.all()
        })

    if tab == "certificates":
        return render(request, "MainApp/profile_tabs/certificates_tab.html", {
            "certificates": profile.certificates.all()
        })

    return render(request, "MainApp/profile_tabs/profile_tab.html", {"profile": profile})


# -------------------- UPLOAD VIDEO --------------------

@login_required
def profile_upload_video(request):
    profile = request.user.profile

    if request.method == "POST":
        title = request.POST.get("title")
        video_file = request.FILES.get("video")
        skills = request.POST.get("skills", "")

        if not video_file:
            return JsonResponse({"success": False, "error": "No video uploaded"})

        video_obj = Video.objects.create(
            uploader=profile,
            title=title,
            video_file=video_file
        )

        for skill in skills.split(","):
            skill = skill.strip()
            if skill:
                s_obj, created = Skill.objects.get_or_create(name=skill)
                video_obj.skills.add(s_obj)

        return JsonResponse({"success": True})

    # GET → return modal form
    return render(request, "MainApp/forms/upload_video_form.html")




# -------------------- UPLOAD CERTIFICATE --------------------

@login_required
def upload_certificate(request):
    profile = request.user.profile

    if request.method == "POST":
        title = request.POST.get("title")
        cert_file = request.FILES.get("certificate")

        if not cert_file:
            return JsonResponse({"success": False, "error": "No certificate uploaded"})

        Certificate.objects.create(
            profile=profile,
            title=title,
            certificate_file=cert_file
        )

        return JsonResponse({"success": True})

    # GET → return modal form
    return render(request, "MainApp/forms/upload_certificate_form.html")

# -------------------- User Profile --------------------
@login_required
def view_user_profile(request, profile_id):
    # Get the Profile object
    other_profile = get_object_or_404(Profile, id=profile_id)

    # Fetch related data
    educations = other_profile.educations.all()
    experiences = other_profile.experiences.all()
    videos = other_profile.videos.all()
    certificates = other_profile.certificates.all()

    return render(request, 'MainApp/user_profile.html', {
        'profile': other_profile,
        'education_list': educations,
        'experience_list': experiences,
        'videos': videos,
        'certificates': certificates,
        'is_owner': False,  # flag to distinguish from own profile
    })
@login_required
def load_user_tab(request, profile_id, tab):
    profile = get_object_or_404(Profile, id=profile_id)

    if tab == "profile":
        return render(request, "MainApp/profile_tabs/profile_tab.html", {
            "profile": profile,
            "educations": profile.educations.all(),
            "experiences": profile.experiences.all(),
        })

    if tab == "videos":
        return render(request, "MainApp/profile_tabs/videos_tab.html", {
            "videos": profile.videos.all()
        })

    if tab == "certificates":
        return render(request, "MainApp/profile_tabs/certificates_tab.html", {
            "certificates": profile.certificates.all()
        })

    return HttpResponse("Invalid Tab")

# -------------------- Add Peer --------------------
@login_required
def add_peer(request, profile_id):
    from_user = request.user.profile
    to_user = get_object_or_404(Profile, id=profile_id)

    if from_user == to_user:
        messages.error(request, "You cannot add yourself.")
        return redirect("user_profile", profile_id=profile_id)

    if Peer.objects.filter(from_user=from_user, to_user=to_user).exists():
        messages.info(request, "Already added.")
        return redirect("user_profile", profile_id=profile_id)

    Peer.objects.create(from_user=from_user, to_user=to_user)
    messages.success(request, "Peer added successfully!")
    return redirect("user_profile", profile_id=profile_id)

# *********************** Expert Functionalites form Here *******************************************


def expert_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, "Invalid username or password.")
            return redirect("expert_login")

        if not user.is_staff:
            messages.error(request, "You are not authorized as an Expert.")
            return redirect("expert_login")

        login(request, user)
        return redirect("expert_home")

    return render(request, "MainApp/expert_login.html")


@login_required
def expert_home(request):
    # Check if expert exists
    try:
        expert = Expert.objects.get(user=request.user)
    except Expert.DoesNotExist:
        messages.error(request, "Expert account not found.")
        return redirect("expert_login")

    # Competitions
    active = Competition.objects.filter(
        expert=expert,
        end_date__gte=timezone.now()
    )

    past = Competition.objects.filter(
        expert=expert,
        end_date__lt=timezone.now()
    )

    return render(request, "MainApp/expert_home.html", {
        "expert": expert,
        "active": active,
        "past": past,
    })

@login_required
def create_competition(request):
    expert = Expert.objects.get(user=request.user)

    if request.method == "POST":
        print("POST skills =", request.POST.getlist("skills"))

    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        start_date = request.POST["start_date"]
        end_date = request.POST["end_date"]
        image = request.FILES.get("image")

        skill_ids = request.POST.getlist("skills")  # this now contains only numeric IDs

        comp = Competition.objects.create(
            expert=expert,
            title=title,
            description=description,
            start_date=start_date,
            end_date=end_date,
            image=image,
        )

        comp.skills.set(skill_ids)

        return redirect("expert_home")

    all_skills = Skill.objects.all()

    return render(request, "MainApp/create_competition.html", {"skills": all_skills})

def user_competitions(request):
    profile = request.user.profile
    skills = profile.skills.all()

    competitions = Competition.objects.filter(skills__in=skills).distinct()

    live = [c for c in competitions if c.is_live()]
    closed = [c for c in competitions if c.is_closed()]

    return render(request, "user_competitions.html", {
        "live": live,
        "closed": closed,
    })
def participate_competition(request, comp_id):
    profile = request.user.profile
    comp = Competition.objects.get(id=comp_id)

    CompetitionParticipation.objects.get_or_create(
        user=profile,
        competition=comp
    )

    return redirect("user_competitions")
