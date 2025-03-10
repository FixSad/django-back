from django.contrib import admin
from .models import *

import pandas as pd
from django.http import HttpResponse
from django.utils.timezone import localtime


@admin.action(description="Export selected results to Excel")
def export_to_excel(modeladmin, request, queryset):
    data = {
        "User": [result.user.username for result in queryset],
        "Test Name": [result.test.test_name for result in queryset],
        "Try Number": [result.try_number for result in queryset],
        "Total Answers": [result.number_all_answers for result in queryset],
        "Correct Answers": [result.number_correct_answers for result in queryset],
        "Complete Time": [localtime(result.complete_time).replace(tzinfo=None) for result in queryset],
        "Accuracy": [result.accuracy for result in queryset],
    }
    df = pd.DataFrame(data)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=test_results.xlsx'
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Results')
    return response


class TestResultsAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'try_number', 'number_all_answers',
                    'number_correct_answers', 'complete_time', 'accuracy')
    actions = [export_to_excel]


admin.site.register(TestResults, TestResultsAdmin)
admin.site.register(TestNSI)
admin.site.register(User)
