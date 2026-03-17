def file_upload(host,filename,token):
    with open(filename,'rb') as infile:
        r=requests.post(host,data={'auth':token},files={'file': infile})
    status=r.json()['status']
    if status!='success':
        raise RuntimeError(f'Upload failed with status {status}')
    else:
        return r.json()['url']
