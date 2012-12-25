from datetime import datetime
import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from teleport.models import File, Directory
from teleport.tasks import bulk_upload_DB, repairDB
import filesystem as fs
from helpers import create_hierarchy
from lib import storage_adapter


def render_json(data):
    response = HttpResponse(json.dumps(data))
    response['Content-Type'] = 'application/json'
    response['Content-Length'] = len(result)
    return HttpResponse(json.dumps())

@csrf_exempt
class ApiHandler(View):
    def put(self, request, *args, **kwargs):
        path = filepath
        remote_path = request.POST['path']
        date_str = str(request.POST['last_modified'])
        last_modified = datetime.strptime(date_str, '%Y-%m-%d')
        f = request.FILES['file']

        temp_path = fs.save_from_upload(remote_path, f)
        file_info = fs.file_info(temp_path)

        remote_parent = os.path.dirname(remote_path)
        
        remote_dir = create_hierarchy(remote_parent)
        new_file = File(name=file_info['name'], path=remote_dir,
                        size=file_info['size'],
                        last_modified=last_modified)
        new_file.save()
        storage_adapter.upload_file(temp_path, remote_path)

        response = render_json({'status': '1', 'message': 'File uploaded successfully.'})
    else:
        response = render_json({'status': '0', 'message': 'Use POST for file uploads.'})
    
    return response

    def delete(self, request, *args, **kwargs):
        path = filepath
        remote_parent = os.path.dirname(remote_path)
        file_name = os.path.basename(remote_path)
        directory = Directory.objects.get(remote_parent)
        file_obj = File.objects.get(path=directory, name=filename)
        file_obj.delete()

        response = render_json({'status': '1', 'message': 'File deleted successfully.'})