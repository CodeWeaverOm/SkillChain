from .models import Profile

class EnsureProfileMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if user.is_authenticated:
            Profile.objects.get_or_create(user=user)
        return self.get_response(request)
