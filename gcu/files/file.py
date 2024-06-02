import os
import uuid

try:
    from google.colab import files
except ImportError:
    class MockColabFiles:
        @staticmethod
        def upload():
            print("Mock function called.")
            return None

    files = MockColabFiles()

class File:
    def __init__(self, **kwargs) -> None:
        self.filename = kwargs.get("filename", None)
        self.path = kwargs.get("path", None)

        self.location = kwargs.get("location", None)
        self.local_path = kwargs.get("local_path", None)
        self.content = kwargs.get("content", None)
        self.ext = kwargs.get("ext", None)
        self.mime = kwargs.get("mime", None)

        


# import mimetypes


# # my_file = gcu.files.File()

# # print(my_file.ext_to_mime("mp3"))

# print(mimetypes.guess_type("test.mp3"))


def upload(path = "", **kwargs) -> File:
    """
    Uploads files to the given path in the current colab session.
    
    Default path is "content/"
    If the path doesn't exist, the path will be created.
    Will return a gcu.files.File object, or a list of gcu.file.File objects if multiple files were uploaded.
    If the upload is cancelled, returns None.

    kwargs
    ----------
    new_filename (str)
        default: None.
        When None, the original file keeps it's name.
        When "_uuid", the filename is updated with a unique name.
        When any other string, the filename is updated (for multiple files, and incremental number is added).

    """

    uploaded = files.upload()

    if uploaded:
        if os.path.isdir(os.path.join("/content", path)) == False:
            os.makedirs(os.path.join("/content", path))

        new_names = list(uploaded.keys())
        if kwargs.get("new_filename", None) == "_uuid":
            new_names = []
            for item in list(uploaded.keys()):
                new_names.append(str(uuid.uuid4()) + os.path.splitext(os.path.basename(item))[1])
        elif isinstance(kwargs.get("new_filename", None), str):
            new_names = []
            if len(list(uploaded.keys())) == 1:
                new_names.append(kwargs.get("new_filename", None) + os.path.splitext(os.path.basename(item))[1])
            else:
                for i, item in enumerate(list(uploaded.keys())):
                    new_names.append(kwargs.get("new_filename", None) + f" {i}" + os.path.splitext(os.path.basename(item))[1])
        
        for i, item in enumerate(list(uploaded.keys())):
            original_path = os.path.join('/content', item)
            new_path = os.path.join("/content", path, new_names[i])
            os.rename(original_path, new_path)

        if len(list(uploaded.keys())) == 1:
            return File(filename = new_names[0], path = os.path.join("/content", path))
        else:
            ret = []
            for filename in new_names:
                ret.append(File(filename = filename, path = os.path.join("/content", path)))
            return ret
    else:
        return None


