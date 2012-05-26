from registration.models import ABTest, TestChoice, TestResult
from django.contrib import admin

admin.site.register(ABTest)
admin.site.register(TestChoice)
admin.site.register(TestResult)
