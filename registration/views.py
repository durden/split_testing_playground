"""
Views for registration app
"""

from django.shortcuts import render


def home(request, template_name="registration/register.html"):
    if request.method == 'POST':
        template_name = 'registration/thanks.html'

    return render(request, template_name)
