import zipfile
import os
import os.path as osp
from config import *
import shutil

def mkdir_if_missing(path):
    if not os.path.exists(path):
        print('mkdir {}'.format(path))
        os.makedirs(path)

def unzip(save_folder, zip_name):
    zip_path = osp.join(save_folder, zip_name)
    # out_dir = save_folder
    # out_dir = osp.join(save_folder, zip_name[:-4])
    out_dir = osp.join(save_folder)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        
        zip_ref.extractall(out_dir)
    
    return out_dir

def zip_dir(src_dir, out_zip):
    # shutil.make_archive(out_zip, 'zip', src_dir)
     shutil.make_archive(out_zip, 'zip', src_dir)

# def save_mot_format(mot_root, gt_file):
#     gt_dir = osp.join(mot_root, 'gt')   
#     os.mkdir(gt_dir)

#     with open(osp.join(gt_dir, 'labels.txt')) as f: 
#         f.write('person')
#         f.close()

#     with open(osp.join(gt_dir, 'gt.txt')) as f:
#         for line

