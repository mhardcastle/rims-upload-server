import sys
import os
os.environ['KEYS']='/home/mjh/.rims-keys'
os.environ['UPLOADS']='/beegfs/rims/downloads'
os.environ['DOWNLOAD']='https://rims.extragalactic.info/downloads/'
sys.path.insert(0, '/home/mjh/git/rims-upload-server')
sys.path.insert(0, '/soft/python3/usr/local/lib64/python3.9/site-packages/')
from upload_server import app as application
