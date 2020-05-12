from __future__ import print_function
import httplib2
import os
import sys

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

# If modifying these scopes, delete your previously saved credentials
SCOPES = 'https://www.googleapis.com/auth/youtube.upload'
CLIENT_SECRET_FILE = 'client_secrets.json'
APPLICATION_NAME = 'youtube-upload'
CREDS_FILENAME = '.youtube-upload-credentials.json'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_path = os.path.join(home_dir,
                                   CREDS_FILENAME)

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store)
    return credentials

def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())

if __name__ == '__main__':
    main()