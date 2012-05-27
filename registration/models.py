from django.db import models


class ABTest(models.Model):
    """Model to hold information about AB split test"""

    name = models.CharField(max_length=300)
    url = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

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


class TestResult(models.Model):
    """Model to hold conversion results of a particular test choice"""

    visitors = models.BigIntegerField()
    conversions = models.BigIntegerField()
    choice = models.ForeignKey(TestChoice)

    def __unicode__(self):
        """return unicode representation of object"""

        return u'Choice: %s, Visitors: %d, Conversions: %d' % (
                    self.choice.description, self.visitors, self.conversions)
