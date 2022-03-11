import os
import sys
apache_dir = os.path.dirname(__file__)
print apache_dir
project = os.path.dirname(apache_dir)
print project
workspace = os.path.dirname(project)
print workspace
print sys.path
