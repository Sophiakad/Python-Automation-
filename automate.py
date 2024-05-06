from os import scandir, rename
from os.path import splitext, exists, join
from shutil import move
from time import sleep

import logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Folders to save downloads to 
source_dir = "/Users/sophiakadegnon/Downloads"
dest_dir_video = "/Users/sophiakadegnon/Desktop/Saved Videos"
dest_dir_image = "/Users/sophiakadegnon/Desktop/Saved Images "
dest_dir_documents = "/Users/sophiakadegnon/Desktop/Saved Docs"

# For distinguishing what type of download is the current item 

# image info
image_info = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw",
                    ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]
# video info 
video_info = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg",
                    ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]
# doc info 
doc_info = [".doc", ".docx", ".odt",
                       ".pdf", ".xls", ".xlsx", ".ppt", ".pptx"]

 
def make_unique(dest, name):
    filename, extension = splitext(name)
    counter = 1
    # if the file already exists, a number is added to the end to make it unique 
    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1

    return name

# Takes in destination folder,entry, and the name  of the file 
# Checks if that file already exists then move entry to a different destination 
def move_file(dest, entry, name):
    if exists(f"{dest}/{name}"):
        unique_name = make_unique(dest, name)
        oldName = join(dest, name)
        newName = join(dest, unique_name)
        rename(oldName, newName)
    move(entry, dest)


class ManageFiles(FileSystemEventHandler):
    # Runs whenever there's a change in "source_dir" 
   
    def on_modified(self, event):
        with scandir(source_dir) as entries:
            # Loops through all files in folder 
            for entry in entries:
                name = entry.name

                self.check_video_files(entry, name)
                self.check_image_files(entry, name)
                self.check_document_files(entry, name)

    def check_video_files(self, entry, name):  # Checks all Video Files
        for video_info in video_info:
            if name.endswith(video_info) or name.endswith(video_info.upper()):
                move_file(dest_dir_video, entry, name)
                logging.info(f"Moved video file: {name}")

    def check_image_files(self, entry, name):  # Checks all Image Files
        for image_info in image_info:
            if name.endswith(image_info) or name.endswith(image_info.upper()):
                move_file(dest_dir_image, entry, name)
                logging.info(f"Moved image file: {name}")

    def check_document_files(self, entry, name):  #  Checks all Document Files
        for doc_info in doc_info:
            if name.endswith(doc_info) or name.endswith(doc_info.upper()):
                move_file(dest_dir_documents, entry, name)
                logging.info(f"Moved document file: {name}")


# Monitors the current directory recursively for file system changes and logs them to the console:
# Initiates entire process
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = ManageFiles()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
