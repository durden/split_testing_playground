"""
Views for registration app
"""

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.utils import timezone

from registration.models import ABTest, TestChoice, TestResult
from registration.models import get_conversion_rate
from registration.forms import RegistrationForm


def conversion_chart(request, test_id):
    """
    Draw simple bar chart depicting conversion rate visually
    """

    # Protect against PIL/reportlab not installed
    try:
        test = ABTest.objects.get(pk=test_id)
    except ABTest.DoesNotExist:
        return HttpResponse(None, 'image/gif')

    choices = TestChoice.objects.filter(test=test)
    chart_data = []
    chart_labels = []

    for choice in choices:
        results = TestResult.objects.filter(choice=choice)

        for result in results:
            conv_rate = get_conversion_rate(result.conversions,
                                            result.visitors)
            chart_data.append(conv_rate)
            chart_labels.append(result.choice.description[0:30])

    try:
        from registration import charts
        d = charts.conversion_chart([chart_data], chart_labels)
    except ImportError:
        return HttpResponse(None, 'image/gif')

    binaryStuff = d.asString('gif')

    return HttpResponse(binaryStuff, 'image/gif')


def _create_result_object(choice_id):
    """Create a TestResult object associated with the given choice_id"""

    try:
        choice_obj = TestChoice.objects.get(pk=choice_id)
    except TestChoice.DoesNotExist:
        return None

    return TestResult(conversions=0, visitors=0, choice=choice_obj)


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


def thanks(request, template_name="registration/thanks.html"):
    """thanks page"""

    return render(request, template_name)


def home(request, template_name="registration/register.html"):
    """Home view"""

    # NOTE: Only using the actual 'django form' on the POST side b/c we could
    # be running split tests on the actual form elements (some are shown and
    # some aren't, etc.).  So, it's just easier to render the form ourselves on
    # the template side.

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if not form.is_valid():
            return render(request, template_name,
                                {'test_choice': int(request.POST['choice']),
                                 'form': form})

        if form.cleaned_data['choice'] > 0:
            choice = form.cleaned_data['choice']

            try:
                result = TestResult.objects.get(pk=choice)
            except TestResult.DoesNotExist:
                result = _create_result_object(choice)

            if result is not None:
                result.conversions += 1
                result.save()

        # NOTE: The data could easily be saved here into the standard django
        # User model or a custom one.  However, the point of this app is just
        # to demonstrate A/B split testing, not saving user information.

        return HttpResponseRedirect('/register/thanks')
    else:
        # See if there's a test running for this url
        choice = _get_choice_for_split_test('registration.views.home')
        if choice > 0:
            try:
                result = TestResult.objects.get(pk=choice)
            except TestResult.DoesNotExist:
                result = _create_result_object(choice)

            if result is not None:
                result.visitors += 1
                result.save()

    return render(request, template_name, {'test_choice': choice})
