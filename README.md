# rims-upload-server

This is a very simple WSGI implementation of an upload server for the distributed RIMS project (https://github.com/saopicc/RIMS). It depends on Flask.

Assumptions:

* You have a web server capable of running WSGI (e.g. Apache)
* You have a virtualhost for RIMS data

## Installation

For testing, set the environment variables KEYS, UPLOADS and DOWNLOAD and then `run python upload_server.py` . This will run the server on your local machine on port 5000. The KEYS environment variable must point to a text file containing at least one key, where keys should be in the format provided by `secrets.token_hex()`. UPLOADS should point to a writable directory. DOWNLOAD should be set to the base URL for downloads.

For production, change the WSGI environment variable settings in `rims.wsgi` and then set up Apache as follows:

```
<VirtualHost *:443>
ServerName MY.RIMS.SERVER.NAME
DocumentRoot "PATH.TO.ROOT"
SSLVerifyClient none
SSLInsecureRenegotiation on
WSGIApplicationGroup %{GLOBAL}
WSGIDaemonProcess rims-upload-server threads=5 display-name=rims-upload-server
WSGIScriptAlias /upload PATH.TO/rims.wsgi
WSGIPassAuthorization On
</VirtualHost>
```

DocumentRoot should be a path to a location that will contain the downloads directory. Make sure both the DocumentRoot and the WSGIScriptAlias are declared as visible to Apache.

## API

It is assumed that downloads are handled by the web server, so the upload server is just responsible for taking files from an authenticated client and storing them in the UPLOADS directory.

There are two endpoints below the WSGIScriptAlias directory:

* `'/'`: call with POST with `auth` set to a valid token from the keys list and the file as multipart form data with name 'file'. The code returns JSON with the result of the upload. A `'status'` string will always be present in the JSON. If `'status'` is `'success'` then a `'url'` string will give the location of the uploaded file.

* `'/keygen'`: call with POST with `auth` set to token 0 from the keys list, and a new token will be generated and added to the keys list (which must therefore be writable to the WSGI process in production). This allows the root user to generate new tokens for non-route users.


