from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import urllib.parse

def photo_transfer(user_id):
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    main_folder_name = 'maraphon'
    existing_folders = drive.ListFile({'q': f"title = '{main_folder_name}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"}).GetList()
    parent_folder_id = [item['id'] for item in existing_folders][0]
    print(parent_folder_id)

    if not existing_folders:
        print('False')
        file_metadata = {
          'title': 'maraphon',
          'mimeType': 'application/vnd.google-apps.folder'
        }

        folder = drive.CreateFile(file_metadata)
        folder.Upload()

    print(user_id)
    existing_folders = drive.ListFile({'q': f"'{parent_folder_id}' in parents and title = '{str(user_id)}' and mimeType = 'application/vnd.google-apps.folder'"}).GetList()

    if not existing_folders:
        print('False')
        file_metadata = {
            'title': f'{str(user_id)}',
            'parents': [{'id': parent_folder_id}],
            'mimeType': 'application/vnd.google-apps.folder'
        }

        folder = drive.CreateFile(file_metadata)
        folder.Upload()
