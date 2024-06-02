import os
import uuid
import requests
import mimetypes
from typing import Union, List

# If working locally, create a mock google.colab package:
try:
    from google.colab import files
except ImportError:
    class MockColabFiles:
        @staticmethod
        def upload():
            print("Mock upload function called")
            return None

    files = MockColabFiles()

class File:
    def __init__(self, **kwargs) -> None:
        """
        An object representing any kind of file.
        """

        self.path = kwargs.get("path", None)
        self.content = kwargs.get("content", None)
        self.filename = kwargs.get("filename", None)
        self.dir = kwargs.get("dir", None)

        # check if online, if so, check if need to dl ?
        # when downloading, will need to update path before next step ?

        if self.path != None:
            self.filename = os.path.basename(self.path)
            self.dir = os.path.dirname(self.path)

        
        self.ext = kwargs.get("ext", None)
        self.mime = kwargs.get("mime", None)
        if self.filename != None:
            self.ext = os.path.splitext(self.filename)[1][1:]
            self.mime = mimetypes.guess_type(self.filename)[0].split("/")

def download(url, path = "", **kwargs) -> Union[File, List[File]]:
    """
    Download media at the given url to the given path in the current colab session.
    
    Default path is "content/". If the path doesn't exist, the path will be created. Will return a gcu.files.File object, or a list of gcu.file.File objects if multiple files were uploaded. If the upload is cancelled, returns None.

    url can be a list of urls.

    kwargs
    ----------
    new_filename (str)
        default: None. When None, the original file keeps it's name. When "_uuid", the filename is updated with a unique name. When any other string, the filename is updated (for multiple files, and incremental number is added).
    range (int)
        default: None
    """

    downloaded = []
    if isinstance(url, str):
        url = [url]
    else:
        for item in url:
            _download_online_file(url, os.path.join("/content", os.path.basename(item)), kwargs.get("range", None))
            downloaded.append(os.path.join("/content", os.path.basename(item)))

    if len(downloaded) > 0:
        return _process_media_get(path, downloaded, kwargs.get("new_filename", None))
    else:
        return None

def upload(path = "", **kwargs) -> Union[File, List[File], None]:
    """
    Uploads files to the given path in the current colab session.
    
    Default path is "content/". If the path doesn't exist, the path will be created. Will return a gcu.files.File object, or a list of gcu.file.File objects if multiple files were uploaded. If the upload is cancelled, returns None.

    kwargs
    ----------
    new_filename (str)
        default: None. When None, the original file keeps it's name. When "_uuid", the filename is updated with a unique name. When any other string, the filename is updated (for multiple files, and incremental number is added).
    """

    # Trigger upload
    uploaded = files.upload()

    if uploaded:
        return _process_media_get(path, list(uploaded.keys()), kwargs.get("new_filename", None))
    else:
        return None

def _download_online_file(url, path, range):
    """Download a file to base colab directory."""
    if range == None:
        response = requests.get(url, stream=True)
    else:
        response = requests.get(url, headers={'Range': f'bytes={range}'}, stream=True)
    if response.status_code == 206 or response.status_code == 200:
        with open(path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)

def _process_media_get(path, file_list, new_filename):
    """Once a file has been retrived, move it and return File objects."""   

    # Create directory if needed
    if os.path.isdir(os.path.join("/content", path)) == False:
        os.makedirs(os.path.join("/content", path))

    # Create a list of new names if needed
    new_names = file_list

    # As uuids
    if new_filename == "_uuid":
        new_names = []
        for item in file_list:
            new_names.append(str(uuid.uuid4()) + os.path.splitext(os.path.basename(item))[1])
    
    # As string
    elif isinstance(new_filename, str):
        new_names = []
        if len(file_list) == 1:
            new_names.append(new_filename + os.path.splitext(os.path.basename(file_list[0]))[1])
        else:
            for i, item in enumerate(file_list):
                new_names.append(new_filename + f" {i}" + os.path.splitext(os.path.basename(item))[1])
    
    # Move uploaded files
    for i, item in enumerate(file_list):
        original_path = os.path.join('/content', item)
        new_path = os.path.join("/content", path, new_names[i])
        os.rename(original_path, new_path)

    # Create File objects
    path_to_add = os.path.join("/content", path)
    if path == "":
        path_to_add = "/content"
    if len(file_list) == 1:
        return File(path = os.path.join(path_to_add, new_names[0]))
    else:
        ret = []
        for filename in new_names:
            ret.append(File(path = os.path.join(path_to_add, filename)))
        return ret