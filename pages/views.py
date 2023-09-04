from django.http import HttpResponse
from django.shortcuts import render
from professionals.models import Professional

# Create your views here.
def home_view(request, *args, **kwargs):
    queryset = Professional.objects.all()[:4]

    context = {
        "motto": "The best platform to offer your professional services on-site",
        "about": "Anywork is a platform that registers professionals to offer their services to needing clients in person. Our services include transportation, tutorship, food and cleaning. Do you have a service to offer? Register with us now!",
        "services": ["Transportation", "Food", "Cleaning", "Tutorship"],
        "object_list": queryset
    }
    return render(request, "home.html", context)

def about_view(request, *args, **kwargs):
    context = {
        "motto": "The best platform to offer your professional services on-site",
        "about": "Anywork is a platform that registers professionals to offer their services to needing clients in person. Our services include transportation, tutorship, food and cleaning. Do you have a service to offer? Register with us now!",
        "services": ["Transportation", "Food", "Cleaning", "Tutorship"],
        "developer": "Tayo Jubril is an aspiring full stack developer with special proclivity for backend development. He is also a product of ALx. He developed 'anywork' web app to create a platform for professionals to offer their services to needing clients on-site. He is also enthusiastic about building more beneficial apps to users all over the world."
    }
    return render(request, "about.html", context)