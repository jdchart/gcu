from gcu import files
import os

# Download a file (or list of files) that is hosted online:
my_colab_file = files.download("https://files.tetras-libre.fr/media/programme_thumb.jpg")

# You can specify a location to upload to (the directory will get created if needed):
uploaded = files.upload("https://files.tetras-libre.fr/media/programme_thumb.jpg", "naughty/folder/path")
uploaded = files.upload("https://files.tetras-libre.fr/media/programme_thumb.jpg", os.path.join("better", "folder", "path"))

# You can also give the file a new name (will add an incremental number to the end if multiple files):
uploaded = files.upload("https://files.tetras-libre.fr/media/programme_thumb.jpg", new_filename = "a new name")

# Or, make it so that each file gets given a unique identifier:
uploaded = files.upload("https://files.tetras-libre.fr/media/programme_thumb.jpg", new_filename = "_uuid")