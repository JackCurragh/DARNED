import os
import sys
apache_dir = os.path.dirname(__file__)
project = os.path.dirname(apache_dir)
workspace = os.path.dirname(project)
if workspace not in sys.path:
	sys.path.append(workspace)
sys.path.append('/home/DATA/Anmol')
sys.path.append('/home/DATA/Anmol/DARNED')
os.environ['DJANGO_SETTINGS_MODULE']='DARNED.settings'
from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()
