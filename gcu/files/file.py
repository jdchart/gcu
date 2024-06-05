import os
import uuid
import requests
import mimetypes
from typing import Union, List
from .text_files import *
from .application_files import *
from .video_files import *
from .audio_files import *
from .image_files import *

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

        properties
        ----------
        path (str)
            path in the google colabs content/ folder
        filename (str)
            just the filename as a string including extension
        dir (str)
            just the folder path as a string
        ext (str)
            file extension
        mime (list)
            the file's mime type (found using mimetypes.guess_type())
        content ()
            the content of the file. This will vary according to file type.

        kwargs
        ----------
        read_content (bool)
            default: False. Run the read_content() function on creation.
        read_kwargs (dict)
            default: None. The kwargs that are passed to the read_content() function.

        methods
        ----------
        read_content()
            retrive the content of the file, the return type changes according to the type of file.
        """

        self.path = kwargs.get("path", None)
        self.filename = kwargs.get("filename", None)
        self.dir = kwargs.get("dir", None)
        self.ext = kwargs.get("ext", None)
        self.mime = kwargs.get("mime", None)

        # If path local given, get filename and directory:
        if self.path != None:
            self.filename = os.path.basename(self.path)
            self.dir = os.path.dirname(self.path)

        # If filename given, get extension and mime type:
        
        if self.filename != None:
            self.ext = os.path.splitext(self.filename)[1][1:]
            self.mime = mimetypes.guess_type(self.filename)[0].split("/")

        self.content = kwargs.get("content", None)

        if kwargs.get("read_content", True):
            if self.filename != None and self.content == None:
                self.read_content(**kwargs.get("read_kwargs", None))

    def read_content(self, **kwargs):
        """
        Retrive the content of the file, the return type changes according to the type of file.
        """

        if self.mime[0] == "image":
            return read_image(self.path)
        elif self.mime[0] == "audio":
            return read_audio(self.path)
        elif self.mime[0] == "video":
            return read_video(self.path)
        elif self.mime[0] == "application":
            if self.mime[1] == "json":
                return read_json(self.path)
            elif self.mime[1] == "xml":
                return read_xml(self.path)
            else:
                return self._cannot_read_data()
        elif self.mime[0] == "text":
            if self.mime[1] == "plain":
                return read_plain_text(self.path)
            elif self.mime[1] == "csv":
                return read_csv(self.path, **kwargs)
            else:
                return self._cannot_read_data()
        else:
            return self._cannot_read_data()
        
    def _cannot_read_data(self):
        """Return none when cannot read content."""

        print("This file type is not supported for content retrieval!")
        return None

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
    read_content (bool)
        default: False. Will run the read_content() function on the File objects once the file is retrieved.
    read_kwargs (dict)
        default: None. The kwargs that are passed to the read_content() function.
    """

    downloaded = []
    if isinstance(url, str):
        url = [url]
    for item in url:
        _download_online_file(item, os.path.join("/content", os.path.basename(item)), kwargs.get("range", None))
        downloaded.append(os.path.join(os.path.basename(item)))

    if len(downloaded) > 0:
        return _process_media_get(path, downloaded, kwargs.get("new_filename", None), read_content = kwargs.get("read_content", False), read_kwargs = kwargs.get("read_kwargs", None))
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
    read_content (bool)
        default: False. Will run the read_content() function on the File objects once the file is retrieved.
    read_kwargs (dict)
        default: None. The kwargs that are passed to the read_content() function.
    """

    # Trigger upload
    uploaded = files.upload()

    if uploaded:
        return _process_media_get(path, list(uploaded.keys()), kwargs.get("new_filename", None), read_content = kwargs.get("read_content", False), read_kwargs = kwargs.get("read_kwargs", None))
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

def _process_media_get(path, file_list, new_filename, **kwargs):
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
        return File(path = os.path.join(path_to_add, new_names[0]), read_content = kwargs.get("read_content", False), read_kwargs = kwargs.get("read_kwargs", None))
    else:
        ret = []
        for filename in new_names:
            ret.append(File(path = os.path.join(path_to_add, filename), read_content = kwargs.get("read_content", False), read_kwargs = kwargs.get("read_kwargs", None)))
        return ret