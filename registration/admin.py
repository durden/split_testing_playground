from registration.models import ABTest, TestChoice, TestResult
from django.contrib import admin


class ABTestAdmin(admin.ModelAdmin):
    list_display = ('name', 'conversion_percentage', 'url', 'start_date',
                    'end_date')


class TestChoiceAdmin(admin.ModelAdmin):
    list_display = ('test_name', 'description')


class TestResultAdmin(admin.ModelAdmin):
    list_display = ('description', 'conversions', 'visitors',
                    'conversion_rate')


admin.site.register(ABTest, ABTestAdmin)
admin.site.register(TestChoice, TestChoiceAdmin)
admin.site.register(TestResult, TestResultAdmin)
