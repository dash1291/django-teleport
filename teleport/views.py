from datetime import datetime
import json
import os.path

from django.conf import settings
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
    result = json.dumps(data)
    response = HttpResponse(result)
    response['Content-Type'] = 'application/json'
    response['Content-Length'] = len(result)
    return response


class ApiHandler(View):
    """
    This is the bare ApiHandler class-based view, which can be used as is, or
    can also be sub-classed and overriden, if additional functionality is 
    required.
    """
    @method_decorator(csrf_exempt)
    def dispatch(self, request, filepath, *args, **kwargs):
        print request.META
        if 'HTTP_TELEPORT_API_SECRET' in request.META:
            api_secret = request.META['HTTP_TELEPORT_API_SECRET']
            if api_secret == settings.TELEPORT['api_secret']:
                return super(ApiHandler, self).dispatch(request, filepath, *args, **kwargs)

        return render_json({'success': False,
                            'message': 'Bad secret key.'})

    def delete(self, request, filepath, *args, **kwargs):
        remote_path = filepath
        remote_parent = os.path.dirname(remote_path)
        file_name = os.path.basename(remote_path)
        try:
            directory = Directory.objects.get(remote_parent)
            file_obj = File.objects.get(path=directory, name=filename)
            file_obj.delete()
            response = render_json({'success': True,
                                    'message': 'File deleted successfully.'})
        except:
            response = render_json({'success': False,
                                    'message': 'The file cannot be deleted.'})
        
        return response

    def post(self, request, filepath, *args, **kwargs):
        remote_path = filepath
        action = request.POST['action']
        remote_parent = os.path.dirname(remote_path)
        file_name = os.path.basename(remote_path)
        
        if action == 'created':
            path = filepath
            date_str = str(request.POST['last_modified'])
            last_modified = datetime.strptime(date_str, '%Y-%m-%d')
            f = request.FILES['file']

            temp_path = filesystem.save_from_upload(path, f)
            file_info = filesystem.file_info(temp_path)

            remote_parent = os.path.dirname(path)
            
            remote_dir = create_hierarchy(remote_parent)
            new_file = File(name=file_info['name'], path=remote_dir,
                            size=file_info['size'],
                            last_modified=last_modified)
            new_file.save()
            storage_adapter.upload_file(temp_path, path)

            response = render_json({'success': True,
                                    'message': 'File uploaded successfully.'})
        
            return response

        try:
            directory = Directory.objects.get(path='/' + remote_parent)
            file_obj = File.objects.get(path=directory, name=file_name)
        except:
            return render_json({'success': False,
                                'message': 'The file does not exist.'})

        if action == 'moved':
            new_path = request.POST['dest']
            parent_path = os.path.dirname(new_path)
            file_name = os.path.basename(new_path)
            parent_path_dir = create_hierarchy(parent_path)
            new_file_obj = File(path=parent_path_dir, name=file_name,
                                last_modified=request.POST['last_modified'],
                                size=file_obj.size)
            new_file_obj.save()
            file_obj.delete()

        elif action == 'modified':
            date_str = str(request.POST['last_modified'])
            last_modified = datetime.strptime(date_str, '%Y-%m-%d')
            file_obj.last_modified = last_modified

            f = request.FILES['file']
            temp_path = filesystem.save_from_upload(remote_path, f)
            storage_adapter.upload_file(temp_path, remote_path)

            #file_obj.size = request.POST['size']
            file_obj.save()

        return render_json({'success': True,
                            'message': 'File updated succesfully.'})