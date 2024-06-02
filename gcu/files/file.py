import os

try:
    from google.colab import files
except ImportError:
    class MockColabFiles:
        @staticmethod
        def upload():
            print("Mock function called.")
            return [""]

    files = MockColabFiles()


def upload(path = ""):
    """
    Uploads files to the given path in the current colab session.
    
    Default path is "content/"
    If the path doesn't exist, the path will be created.
    Will return a gcu.files.File object, or a list of gcu.file.File objects if multiple files were uploaded.
    If the upload is cancelled, returns None.
    """

    uploaded = files.upload()

    if uploaded != None:
        if os.path.isdir(os.path.join("/content", path)) == False:
            os.makedirs(os.path.join("/content", path))
        
        for filename in uploaded.keys():
            original_path = os.path.join('/content', filename)
            new_path = os.path.join("/content", path, filename)
            os.rename(original_path, new_path)

        if len(list(uploaded.keys()) == 1):
            return File(path = list(uploaded.keys())[0])
        else:
            ret = []
            for filename in uploaded:
                ret.append(File(path = filename))
            return ret
    else:
        return None


class File:
    def __init__(self, **kwargs) -> None:
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