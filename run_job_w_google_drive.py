from __future__ import print_function
import httplib2
import os
from subprocess import call

from apiclient import discovery
from apiclient import errors
from apiclient import http

import oauth2client
from oauth2client import client
from oauth2client import tools

from constants import *

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatability with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def get_drive_service():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v2', http=http)
    return service

def get_file_metadata(service, file_id):
  """Print a file's metadata.

  Args:
    service: Drive API service instance.
    file_id: ID of the file to print metadata for.
  """
  try:
    file = service.files().get(fileId=file_id).execute()
    return file
  except errors.HttpError, error:
    print('An error occurred: %s' % error)

def download_file(service, file_id, local_fd):
  """Download a Drive file's content to the local filesystem.

  Args:
    service: Drive API Service instance.
    file_id: ID of the Drive file that will downloaded.
    local_fd: io.Base or file object, the stream that the Drive file's
        contents will be written to.
  """
  request = service.files().get_media(fileId=file_id)
  media_request = http.MediaIoBaseDownload(local_fd, request)

  while True:
    try:
      download_progress, done = media_request.next_chunk()
    except errors.HttpError, error:
      print ('An error occurred: %s' % error)
      return
    if download_progress:
      print('Download Progress: %d%%' % int(download_progress.progress() * 100))
    if done:
      print('Download Complete')
      return

def upload_file(service, filename, mimeType):
    body = {
      'title': filename,
      'description': "DESC OF " + filename
    }

    media_body = http.MediaFileUpload(filename, mimetype=mimeType, resumable=True)
    request = service.files().insert(body=body, media_body=media_body)
    response = None
    while response is None:
      status, response = request.next_chunk()
      if status:
        print("Uploaded %d%%." % int(status.progress() * 100))
    print("Upload Complete!")

def get_file_id_by_filename(service, filename):
    service = get_drive_service()

    results = service.files().list(maxResults=10).execute()
    items = results.get('items', [])
    for item in items:
        if (item['title'] == filename):
            print("FILE_ID = %s" % item["id"])
            return item["id"]
    return None

def run_vaa3d_script(input_filename, output_filename):
    plugin_name=VAA3D_PLUGIN
    func_name=FUNC_NAME
    print("Tracing neuron...");
    call([VAA3D_PATH, "-x", plugin_name, "-f", func_name, "-i", input_filename, "-o", output_filename])
    print("Trace complete!")
    return output_filename

def run_vaa3d_job(service, input_filename, output_filename):
    input_file_id = get_file_id_by_filename(service, input_filename)
    input_file = open(input_filename,'w')
    input_file = download_file(service, input_file_id, input_file)
    output_filename = run_vaa3d_script(input_filename, output_filename)
    upload_file(service, output_filename, MIME_TYPE)

def upload_test_file(service):
    """Upload test file to your Google Drive account"""
    upload_file(service, TEST_INPUT_FILENAME, MIME_TYPE)

if __name__ == '__main__':
    service = get_drive_service()
    upload_test_file(service) #comment this out after test file is in your Google Drive
    run_vaa3d_job(service, TEST_INPUT_FILENAME, TEST_OUTPUT_FILENAME)

