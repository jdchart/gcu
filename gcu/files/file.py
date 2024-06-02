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


def upload(path = "/"):
    """
    Uploads files to the given path in the current colab session.
    
    If the path doesn't exist, the path will be created.
    Will return a gcu.files.File object, or a list of gcu.file.File objects
    if multiple files were uploaded.
    """

    uploaded = files.upload()
    uploaded = list(uploaded.keys())

    if os.path.isdir(path) == False:
        os.makedirs(path)

    print(uploaded)
    
    # for filename in uploaded.keys():
    #     # Construct the full path of the uploaded file
    #     original_path = os.path.join('/content', filename)
    #     # Construct the new path
    #     new_path = os.path.join(target_directory, filename)
    #     # Move the file
    #     os.rename(original_path, new_path)


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