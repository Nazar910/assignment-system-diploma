from django.shortcuts import render, redirect, get_list_or_404
from django.http import HttpResponseNotFound, HttpResponse
from django.forms import ModelForm
from django.contrib.auth.decorators import login_required
from django import forms
from django.core import serializers

from assignment_system.models import AssignmentEvent


def assignments_finished_list(request):
    accept_json = request.META['HTTP_ACCEPT'] == 'application/json'
    if request.method != 'GET' or not accept_json:
        return HttpResponseNotFound('Not found!')

    assignments_events = get_list_or_404(AssignmentEvent, event_type=AssignmentEvent.FINISHED)
    return HttpResponse(serializers.serialize('json', assignments_events))
