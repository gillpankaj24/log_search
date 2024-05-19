import dropbox
from dropbox.exceptions import AuthError

DROPBOX_ACCESS_TOKEN = ''


def dropbox_connect():
    """Create a connection to Dropbox."""
    try:
        dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
    except AuthError as e:
        print('Error connecting to Dropbox with access token: ' + str(e))
    return dbx


def dropbox_list_files(dbx, path):
    """Return files in a given Dropbox folder path in the Apps directory."""
    files = dbx.files_list_folder(path).entries
    return files


def dropbox_download_file(dbx, path):
    """Returns content of a file"""
    try:
        md, res = dbx.files_download(path)
    except dropbox.exceptions.HttpError as err:
        print('*** HTTP error', err)
        return None
    data = res.content
    return data.decode("utf-8")
