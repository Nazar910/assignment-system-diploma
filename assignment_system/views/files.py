from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.core.files.storage import Storage
from django.utils.encoding import smart_str
from filetransfers.api import serve_file
import os

from assignment_system.models import Message


def download_file(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    return serve_file(request, message.file)
