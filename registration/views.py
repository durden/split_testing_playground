"""
Views for registration app
"""

from django.http import HttpResponse
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.utils import timezone

from registration.models import ABTest, TestChoice, TestResult
from registration.models import get_conversion_rate


def conversion_chart(request, test_id):
    """
    Draw simple bar chart depicting conversion rate visually
    """

    # Protect against PIL/reportlab not installed
    try:
        from registration import charts
        d = charts.ConversionChart()
    except ImportError:
        return HttpResponse(None, 'image/gif')

    test = ABTest.objects.get(pk=test_id)
    choices = TestChoice.objects.filter(test=test)
    chart_data = []

    for choice in choices:
        results = TestResult.objects.filter(choice=choice)

        for result in results:
            conv_rate = get_conversion_rate(result.conversions,
                                            result.visitors)
            chart_data.append(conv_rate)

    d.bar.data = [chart_data]
    binaryStuff = d.asString('gif')

    return HttpResponse(binaryStuff, 'image/gif')


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
    """Home view"""

    if request.method == 'POST':
        choice = request.POST['choice']
        if choice > 0:
            result = TestResult.objects.get(pk=choice)
            result.conversions += 1
            result.save()

        template_name = 'registration/thanks.html'
    else:
        # See if there's a test running for this url
        choice = _get_choice_for_split_test('registration.views.home')
        if choice > 0:
            result = TestResult.objects.get(pk=choice)
            result.visitors += 1
            result.save()

    return render(request, template_name, {'test_choice': choice})
