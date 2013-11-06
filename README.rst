django-teleport
===============

Re-usable Django app for filesystem sychronization.

It needs a proper client for the whole filesystem synchronization thing to work. Without such a client, this merely does file uploads.

For the client, see teleport-client_

.. _teleport-client: https://github.com/dash1291/teleport-client

Installation
------------

``pip install -e git+https://github.com/dash1291/django-teleport#egg=django-teleport``

After it has been installed, add ``teleport`` to the ``INSTALLED_APPS`` setting of your Django project and run ``python manage.py syncdb``, which will create some required models.

Configuration
-------------

For a minimal configuration that uses local filesystem for storage, add the following to your ``settings.py`` file.

::

    TELEPORT = {
        'api_secret': 'a random string',
        'storage_type': 'local',
        'storage_path': 'absolute/path/to/storage/directory'
    }

    TEMP_FILE_STORE = 'absolute/path/to/temporary/directory'

You will also need to configure your URLConf to pick teleport urls. For that you can do something like this in your ``urls.py``:

::

    from teleport.urls import urlpatterns as teleport_patterns


    urlpatterns = patterns('',
        url('r^teleport/', include(teleport_patterns),
    )
