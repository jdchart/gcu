from gcu import files
import os

# Use the upload() function to upload files, and return a File class object, or list of File class object:
uploaded = files.upload()

# You can specify a location to upload to (the directory will get created if needed):
uploaded = files.upload("naughty/folder/path")
uploaded = files.upload(os.path.join("better", "folder", "path"))

# You can also give the file a new name (will add an incremental number to the end if multiple files):
uploaded = files.upload(new_filename = "a new name")

# Or, make it so that each file gets given a unique identifier:
uploaded = files.upload(new_filename = "_uuid")