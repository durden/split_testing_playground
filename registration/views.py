"""
Views for registration app
"""

from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.utils import timezone

from registration.models import ABTest, TestChoice, TestResult


# TODO: Might be a clever way to turn this into a decorator and just slap it on
# view functions and 'do the right thing'
def _get_choice_for_split_test(view_function):
    """
    Get a choice_id for a split test associated with the given view function

    view_function can be direct reference to view function or string of
    function
    Example: 'registration.views.home'

    If no split test is running for the given url, 0 will be returned.
    """

    # choice_id 0 will show the 'control' in template so if no split test is
    # running users will automatically see the regular template
    choice = 0

    tests = ABTest.objects.filter(url=reverse(view_function))
    for test in tests:
        now = timezone.now()
        if test.start_date <= now and test.end_date > now:
            choices = TestChoice.objects.filter(test=test)
            results = TestResult.objects.filter(choice__in=list(choices))
            num_results = sum([result.visitors for result in results])

            # Evenly distribute test across all choices by modding by
            # number of results for the entire test
            choice = choices[num_results % len(choices)].id

    return choice


def home(request, template_name="registration/register.html"):
    if request.method == 'POST':
        template_name = 'registration/thanks.html'
    else:
        # See if there's a test running for this url
        choice = _get_choice_for_split_test('registration.views.home')

    return render(request, template_name, {'test_choice': choice})
