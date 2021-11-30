import streamlit as st
import pandas as pd
import numpy as np
from config import *
import os
import requests

from utils.merge_gt_to_mot_gt import merge_gt_to_mot_gt
from utils.mot_gt_to_merge_gt import mot_gt_to_merge_gt
from utils.utils import unzip

def load_session():
    return requests.Session()

def save_uploadedfile(uploadedfile):
    file = uploadedfile.name

    name, ext = file.split('.')[0], file.split('.')[1]

    if not os.path.exists(SAVE_FOLDER):
        os.makedirs(SAVE_FOLDER)

    save_path = os.path.join(SAVE_FOLDER, file)
    
    if os.path.exists(save_path):
        save_path = os.path.join(SAVE_FOLDER, name + "_{}.{}".format(len(os.listdir(SAVE_FOLDER)), ext))

    with open(save_path,"wb") as f:
            f.write(uploadedfile.getbuffer())

    return save_path

def main():
    st.title("Convert annotation from single views to multiple view")

    upload_file = st.file_uploader("Upload your zip folder that contains gt.txt files of all views:", type=SUPPORT_FORMAT)

    col1, col2, col3, col4, col5, col6_7, col8, col9, col10, col11 = st.columns([1,1,1,1,1,2,1,1,1,1])

    if upload_file is not None and col6_7.button('Process file'):
        saved_path = save_uploadedfile(upload_file)

        out_file = mot_gt_to_merge_gt(gt_zip=saved_path)
        print('out_file', out_file)

        # download zip file
        with open(out_file, "rb") as fp:
            btn = st.download_button(
                label="Download ZIP",
                data=fp,
                file_name="multiple_view_mot.zip",
                mime="application/zip"
            )

    
    st.title("Convert annotation from multiple view to single views")

    upload_file = st.file_uploader("Upload your zip folder in Datumaru format:", type=SUPPORT_FORMAT)

    col1, col2, col3, col4, col5, col6_7, col8, col9, col10, col11 = st.columns([1,1,1,1,1,2,1,1,1,1])

    if upload_file is not None and col6_7.button('Process file'):
        saved_path = save_uploadedfile(upload_file)

        out_file = merge_gt_to_mot_gt(gt_zip=saved_path)

        # download zip file
        with open(out_file, "rb") as fp:
            btn = st.download_button(
                label="Download ZIP",
                data=fp,
                file_name="single_views_mot.zip",
                mime="application/zip"
            )

if __name__ == "__main__":
    main()

