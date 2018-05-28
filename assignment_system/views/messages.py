from django.http import HttpResponse
from django.shortcuts import get_object_or_404, get_list_or_404
from django.core import serializers

from assignment_system.models import Message, Assignment, Assignee


def create_message(request):
    file = None
    if 'file' in request.FILES:
        file = request.FILES['file']
    text = request.POST.get('text')
    assignment_id = request.POST.get('assignment_id')
    assignment = get_object_or_404(Assignment, id=assignment_id)

    user = request.user
    assignee = get_object_or_404(Assignee, email=user.email)

    message = Message(
        file=file,
        text=text,
        assignment=assignment,
        author=assignee,
        author_full_name=assignee.name + ' ' + assignee.last_name
    )
    message.save()

    return HttpResponse(serializers.serialize('json', [message]))


def get_messages_by_assigmnent_id(request, id):
    messages = get_list_or_404(Message, assignment_id=id)
    return HttpResponse(serializers.serialize('json', messages))
