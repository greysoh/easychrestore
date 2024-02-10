import os
from urllib import request

def download(url: str, dest_folder: str):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)  # create folder if it does not exist

    filename = url.split('/')[-1].replace(" ", "_")  # be careful with file names
    file_path = os.path.join(dest_folder, filename)

    try:
        with request.urlopen(url) as response, open(file_path, 'wb') as out_file:
            data = response.read(1024 * 8)
            while data:
                out_file.write(data)
                data = response.read(1024 * 8)
    except Exception as e:
        print("Download failed:", e)