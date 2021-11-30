import os 
import os.path as osp
import glob
from utils.utils import *

from utils.utils import zip_dir

# since all gt files have id started with 1, we need to increase id from 
# second gt files to avoid conflicting
def find_max_id(path):
    with open(path, "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
        lines = [line.split(",") for line in lines]
        max_id = len(set([line[1] for line in lines]))
    return max_id

def mkdir_if_missing(path):
    if not osp.exists(path):
        print('mkdir {}'.format(path))
        os.makedirs(path)

def process_object_gt(line, current_total_id, position, frame_shape):
    # this function is use to update new id and new coordinate for object gt
    height, width = frame_shape

    line = line.strip()
    line = line.split(",")
    line[1] = str(int(line[1]) + current_total_id)

    if position == "top left":
        cam_id = 1
    elif position == "top right":
        cam_id = 2
        # bbox left
        line[2] = str(float(line[2]) + width)
    elif position == "bottom left":
        cam_id = 3
        # bbox top
        line[3] = str(float(line[3]) + height)
    elif position == "bottom right":
        cam_id = 4
        # bbox left
        line[2] = str(float(line[2]) + width)
        #
        line[3] = str(float(line[3]) + height)

    # replace 6th element in line with cam id
    line[6] = str(cam_id)
    return line

def reformat_line(line):
    # take line in array format as input
    return "{},{},{},{},{},{},{},{},{}\n".format(
        line[0], line[1], line[2], line[3], line[4], line[5], line[6], \
        line[7], line[8]
    )

def get_frame_idx(line):
    return int(line[0])

def mot_gt_to_merge_gt(gt_zip, out_dir):
    vid_pos = ["top left", "top right", "bottom left", "bottom right"]

    # gt_list = [osp.join(gt_dir, gt) for gt in sorted(os.listdir(gt_dir))]
    gt_dir = unzip(save_folder=SAVE_FOLDER, zip_name=os.path.basename(gt_zip))

    gt_list = glob.glob("{}/*.txt".format(gt_dir))

    frame_shape = (1080, 1920)

    current_total_id = 0

    merge_content = []

    max_id = 1

    for idx, path in enumerate(gt_list):
        position = vid_pos[idx]

        with open(path, "r") as f:
            lines = f.readlines()
            lines = [
                process_object_gt(line,current_total_id,position,frame_shape)
                for line in lines
            ]

            merge_content.extend(lines)

        max_id = find_max_id(path)
        current_total_id += max_id

    merge_content.sort(key=get_frame_idx)
    merge_content = [reformat_line(line) for line in merge_content]

    '''
    Write to MOT format 
    '''
    print('out_dir', out_dir)
    mkdir_if_missing(out_dir)
    os.mkdir(osp.join(out_dir, 'gt'))
    out_label = osp.join(out_dir, "gt/labels.txt")
    out_gt = osp.join(out_dir, 'gt/gt.txt')
    
    with open(out_label, 'w') as f: 
        f.write('person')
        f.close()

    with open(out_gt, "w") as f:
        for line in merge_content:
            f.write(line)

    zip_dir(src_dir=out_dir, out_zip=out_dir)

    return out_dir + '.zip'
