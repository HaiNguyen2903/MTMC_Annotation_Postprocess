import zipfile
import os
import os.path as osp
from config import *
from utils.utils import *
from utils.mot_gt_to_merge_gt import *

zip_file = 'test_streamlit.zip'
gt_dir = '/Users/hainguyen/Documents/deep_learning_projects/streamlit/save_dir/test_streamlit'
out_dir = '/Users/hainguyen/Documents/deep_learning_projects/streamlit/save_dir/test_streamlit/merge'

# out = mot_gt_to_merge_gt(gt_dir, out_dir)
# print(out)

zip_dir(src_dir='test_zip', out_zip='anc')
