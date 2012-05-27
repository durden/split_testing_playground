"""
Views for ab_testing project
"""

from django.shortcuts import render


def home(request, template_name="home.html"):
    return render(request, template_name)


def about(request, template_name="about.html"):
    return render(request, template_name)
