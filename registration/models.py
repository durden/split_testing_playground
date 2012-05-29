from django.db import models


def get_conversion_rate(conversions, visits):
    """Get conversion rate"""
    try:
        conv_rate = round((conversions / float(visits)) * 100, 4)
    except ZeroDivisionError:
        conv_rate = None

    return conv_rate


class ABTest(models.Model):
    """Model to hold information about AB split test"""

    name = models.CharField(max_length=300)
    url = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def conversion_percentage(self):
        """Return overall conversion rate of test"""

        choices = TestChoice.objects.filter(test=self)
        results = TestResult.objects.filter(choice__in=list(choices))
        visits = sum([result.visitors for result in results])

        conversions = sum([result.conversions for result in results])
        return get_conversion_rate(conversions, visits)

    def __unicode__(self):
        """return unicode representation of object"""

        return u'%s' % (self.name)


class TestChoice(models.Model):
    """
    Model to hold information about various test 'choices' that are associated
    with a single ABTest object
    """

    test = models.ForeignKey(ABTest)
    description = models.TextField()

    def __unicode__(self):
        """return unicode representation of object"""

        return u'%s' % (self.description)

    def test_name(self):
        """Get name of test choice is associated with"""

        return self.test.name


class TestResult(models.Model):
    """Model to hold conversion results of a particular test choice"""

    visitors = models.BigIntegerField()
    conversions = models.BigIntegerField()
    choice = models.ForeignKey(TestChoice)

    def description(self):
        """Get description of choice result is associated with"""

        return self.choice.description

    def conversion_rate(self):
        """Get conversion rate as percentage"""

        return get_conversion_rate(self.conversions, self.visitors)

    def __unicode__(self):
        """return unicode representation of object"""

        return u'Choice: %s, Visitors: %d, Conversions: %d, Rate: %s %%' % (
                    self.choice.description, self.visitors, self.conversions,
                    get_conversion_rate(self.conversions, self.visitors))
