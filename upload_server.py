import os
from flask import Flask, request
from uuid import uuid4
import secrets

UPLOADS=os.environ['UPLOADS']
DOWNLOAD=os.environ['DOWNLOAD']
keys=[k.rstrip() for k in open(os.environ['KEYS']).readlines()]

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        auth=request.form.get('auth')
        if auth is None:
            return {'status':'unauthorized'}
        if auth not in keys:
            return {'status':'unauthorized'}
        if 'file' not in request.files:
            return {'status':'failed'}
        upload_file=request.files['file']
        if upload_file is None:
            return {'status':'failed'}
        filename=str(uuid4()) # hopefully unique ID -- 128 bits
        try:
            upload_file.save(os.path.join(UPLOADS,filename))
        # try to catch all write errors
        except (IOError,PermissionError) as e:
            return {'status':'failed','description':str(e)}
        return {'status':'success','url':DOWNLOAD+filename}
    else:
        return {'status':'bad method'}

@app.route('/keygen', methods=['GET', 'POST'])
def keygen():
    if request.method == 'POST':
        auth=request.form.get('auth')
        if auth is None:
            return {'status':'unauthorized'}
        if keys[0]!=auth:
            return {'status':'unauthorized'}
        key=secrets.token_hex()
        keys.append(key)
        with open(os.environ['KEYS'],'a') as outfile:
            outfile.write(key+'\n')
        return {'status':'success','key':key}
    
if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0')
    
