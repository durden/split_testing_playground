"""
Views for ab_testing project
"""

from django.shortcuts import render


def home(request, template_name="home.html"):
    """homepage"""

    return render(request, template_name)


def about(request, template_name="about.html"):
    """about page"""

    return render(request, template_name)
