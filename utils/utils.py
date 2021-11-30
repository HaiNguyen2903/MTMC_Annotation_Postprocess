import zipfile
import os
import os.path as osp
from config import *
import shutil

zip_file = 'test_streamlit.zip'

def unzip(save_folder, zip_name):
    zip_path = osp.join(save_folder, zip_name)
    out_dir = save_folder

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        
        zip_ref.extractall(out_dir)

    return osp.join(out_dir, zip_name.split('.')[0])

def zip_dir(src_dir, out_zip):
    shutil.make_archive(out_zip, 'zip', src_dir)

