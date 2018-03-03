from django.shortcuts import render

from assignment_system.models import Assignment


def assignments_list(request):
    assignments = Assignment.objects.all()
    context = {
        'assignees': assignments
    }
    return render(request, 'assignment_system/assignments.html')