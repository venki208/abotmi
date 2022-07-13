import logging

from mimetypes import MimeTypes

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.core.files.storage import default_storage

logger = logging.getLogger(__name__)


def get_protected_media(request):
    mime = MimeTypes()
    file_path = request.path_info
    file_path = file_path.split('media/')[1]
    contenttype = mime.guess_type(file_path)[0]
    _file = default_storage.open(file_path,'r')
    return FileResponse(_file.read(), content_type=contenttype)
