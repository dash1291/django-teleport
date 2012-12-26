from datetime import datetime
import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.utils.decorators import method_decorator

from teleport.helpers import create_hierarchy
from teleport.lib import filesystem, storage
from teleport.models import File, Directory

storage_adapter = storage.get_adapter()

def render_json(data):
    response = HttpResponse(json.dumps(data))
    response['Content-Type'] = 'application/json'
    response['Content-Length'] = len(result)
    return HttpResponse(json.dumps())


class ApiHandler(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ApiHandler, self).dispatch(*args, **kwargs)

    def put(self, request, *args, **kwargs):
        path = filepath
        remote_path = request.POST['path']
        date_str = str(request.POST['last_modified'])
        last_modified = datetime.strptime(date_str, '%Y-%m-%d')
        f = request.FILES['file']

        temp_path = filesystem.save_from_upload(remote_path, f)
        file_info = filesystem.file_info(temp_path)

        remote_parent = os.path.dirname(remote_path)
        
        remote_dir = create_hierarchy(remote_parent)
        new_file = File(name=file_info['name'], path=remote_dir,
                        size=file_info['size'],
                        last_modified=last_modified)
        new_file.save()
        storage_adapter.upload_file(temp_path, remote_path)

        response = render_json({'status': '1', 'message': 'File uploaded successfully.'})
    
        return response

    def delete(self, request, *args, **kwargs):
        path = filepath
        remote_parent = os.path.dirname(remote_path)
        file_name = os.path.basename(remote_path)
        directory = Directory.objects.get(remote_parent)
        file_obj = File.objects.get(path=directory, name=filename)
        file_obj.delete()

        response = render_json({'status': '1', 'message': 'File deleted successfully.'})

    def post(self, request, *args, **kwargs):
        path = filepath
        action = request.POST['action']
        remote_parent = os.path.dirname(remote_path)
        file_name = os.path.basename(remote_path)
        directory = Directory.objects.get(remote_parent)
        file_obj = File.objects.get(path=directory, name=filename)
        
        if action == 'moved':
            new_path = request.POST['dest']
            path = os.path.dirname(new_path)
            file_name = os.path.basename(new_path)
            path_dir = Directory.objects.get(path)
            new_file_obj = File(path=path_dir, name=file_name,
                                last_modified=request.POST['last_modified'],
                                size=file_obj.size)
            new_file_obj.save()
            file_obj.delete()

        elif action == 'modified':
            file_obj.last_modified = request.POST['last_modified']
            file_obj.size = request.POST['size']

        return render_json({'status': '1', 'message': 'File updated succesfully.'})