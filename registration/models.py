from django.db import models


class ABTest(models.Model):
    """Model to hold information about AB split test"""

    name = models.CharField(max_length=300)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()


class TestChoice(models.Model):
    """
    Model to hold information about various test 'choices' that are associated
    with a single ABTest object
    """

    test = models.ForeignKey(ABTest)
    description = models.TextField()


class TestResult(models.Model):
    """Model to hold conversion results of a particular test choice"""


    visitors = models.BigIntegerField()
    conversions = models.BigIntegerField()
    choice = models.ForeignKey(TestChoice)
