from Google import Create_Service
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload
import io
import os
import pandas as pd

CLIENT_SECRET_FILE = 'client_secret.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

def update(file_name:str, new_file_name:str, mime_type:str, folder_id:str, old_file_id):
    file_metadata = {
        'name': new_file_name,
        'parents': [folder_id]
    }

    media_content = MediaFileUpload(file_name, mimetype = mime_type)
    service.files().update(fileId=old_file_id, media_body=media_content).execute()

def list_files(folder_id = '1nj1nzovmwUneexkinlKncUqYoPNj38sS'):
    query = f"parents = '{folder_id}'"

    response = service.files().list(q=query).execute()
    files = response.get('files')
    nextPageToken = response.get('nextPageToken')

    while nextPageToken:
        response = service.files().list(q=query, pageToken=nextPageToken).execute()
        files.extend(respond.get('files'))
        nextPageToken = response.get('nextPageToken')

    pd.set_option('display.max_columns', 100)
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.min_rows', 500)
    pd.set_option('display.max_colwidth', 150)
    pd.set_option('display.width', 200)
    pd.set_option('expand_frame_repr', True)
    return pd.DataFrame(files)

def get_id(folder_df, name:str):
    id = folder_df[folder_df['name'] == name]
    return id.iloc[0,1]

def get_all_ids(folder_df, date:str):
    valid = []
    rows = len(folder_df.index)
    for i in range(rows):
        find = folder_df.iloc[i,2].find(date)
        if find == 0:
            valid.append((folder_df.iloc[i,1],folder_df.iloc[i,2]))
    return valid

def download_files(id:str, file_name:str, save_as:str):
    request = service.files().get_media(fileId=id)

    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fd=fh, request = request)
    done = False

    while not done:
        status, done = downloader.next_chunk()
        
    fh.seek(0)
    with open(os.path.join(save_as, file_name), 'wb') as f:
        f.write(fh.read())
        f.close()

def find_and_download(folder_id:str, file_name:str, save_as:str):
    folder_df = list_files(folder_id)
    id = get_id(folder_df, file_name)
    download_files(id, file_name, save_as)

def find_and_download_all(folder_id:str, date:str, save_as:str)->bool:
    folder_df = list_files(folder_id)
    valid_ids = get_all_ids(folder_df,date)
    if len(valid_ids) == 0:
        return False
    for i in valid_ids:
        download_files(i[0],i[1],save_as)
    return True

if __name__ == '__main__':
    file_name = 'Drive_folder/password.txt'
    old_file_id = '1qvANpdJH0g5_yKyT2O84V2I9nYvxMWpL'
    root_id = '1nj1nzovmwUneexkinlKncUqYoPNj38sS'
    update(file_name, 'password.txt','text/plain',root_id,old_file_id)