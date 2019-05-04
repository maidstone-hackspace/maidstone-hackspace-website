"""
WSGI config for Maidstone Hackspace project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os
import bjoern
import socket

from django.core.wsgi import get_wsgi_application

# We defer to a DJANGO_SETTINGS_MODULE already in the environment. This breaks
# if running multiple sites in the same mod_wsgi process. To fix this, use
# mod_wsgi daemon mode with each site in its own daemon process, or use
# os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings.production"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
application = get_wsgi_application()

# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)
# apply Werkzeug WSGI middleware
# if os.environ.setdefault('DJANGO_DEBUG', 'False') is True:

from werkzeug.debug import DebuggedApplication
application = DebuggedApplication(application, evalex=True, pin_security=True, pin_logging=True)
application.debug = True

# bjoern.run(application, 'unix:/data/sockets/bjoern-mhackspace.sock')
#https://stackoverflow.com/questions/46301706/bjoern-wsgi-server-unix-socket-permissions

# class ReloadApplicationMiddleware(object):
#     def __call__(self, *args, **kwargs):
#         print('Reloading...')
#         self.app = self.import_func()
#         return self.app(*args, **kwargs)

# application = ReloadApplicationMiddleware(application)


socket_path = '/data/sockets/maidstone-hackspace.sock'
if os.path.exists(socket_path):
    os.unlink(socket_path)

sock = socket.socket(socket.AF_UNIX)
sock.bind(socket_path)
sock.listen(1024)
os.chmod(socket_path, 0o666)

try:
    bjoern.server_run(sock, application)
except KeyboardInterrupt:
    os.unlink(sock.getsockname())
    sock.close()
