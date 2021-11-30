import json
import os 
import os.path as osp
import argparse

parser = argparse.ArgumentParser(description="Arguments for converting \
                                              Datumaru multi view gt file \
                                              into separate MOT gt files")

parser.add_argument("--merge_gt", default="/Users/hainguyen/Documents/deep_learning_projects/mtmc_annotate/fusing_multi_view/gt/scene_3/multi_view_4125_4126/default.json",
                                type=str,
                                help="json gt path")

parser.add_argument("--output_dir", default="/Users/hainguyen/Documents/deep_learning_projects/mtmc_annotate/generate_top_view/sence3/",  
                                type=str, 
                                help="output dir to contain separate MOT \
                                      files for each view")

parser.add_argument("--view_shape", default=(1920, 1080), type=tuple)

args = parser.parse_args()

view_shape = args.view_shape

def mkdir_if_missing(dir_path):
    if not os.path.exists(dir_path):
        print("Make dir in {}".format(dir_path))
        os.makedirs(dir_path)

def get_view_id(bbox, view_shape=view_shape):
    # each view is define as left top and width height
    # return view id
    width, height = view_shape

    view_coordinates = {
        "view_1": {"left":0,"top":0,"width":width,"height":height},
        "view_2": {"left":width,"top":0,"width":width,"height":height},
        "view_3": {"left":0,"top":height,"width": width,"height":height},
        "view_4": {"left":width,"top":height,"width":width,"height":height},
    }

    bbox_left, bbox_top, bbox_width, bbox_height = bbox

    # handle view 1 and view 2
    if bbox_top < view_coordinates["view_3"]["top"]:
        if bbox_left < view_coordinates["view_2"]["left"]:
            return 1
        else:
            return 2
    else:
        if bbox_left < view_coordinates["view_4"]["left"]:
            return 3
        else:
            return 4

def get_original_coordinate(bbox, view_id, view_shape=args.view_shape):
    width, height = view_shape

    left, top = bbox[0], bbox[1]

    if view_id == 2:
        left = left - width
        bbox[0] = left
    if view_id == 3: 
        top = top - height
        bbox[1] = top
    if view_id == 4: 
        left = left - width
        top = top - height
        bbox[0], bbox[1] = left, top

    return bbox

def get_global_id(obj_list, id_groups):
    for obj in obj_list:
        obj_id = int(obj[1])

        for idx, group_id in enumerate(id_groups.values()):
            if obj_id in group_id:
                obj_id = idx + 1
                obj[1] = obj_id
                break

    return obj_list

def get_view_objects(merge_gt):
    # get object for each view
    view_objects = {
        "view_1": [],
        "view_2": [],
        "view_3": [],
        "view_4": []
    }

    # get a dictionary, where keys are group id and values are tracking id 
    groups = {}

    f = open(merge_gt)

    data = json.load(f)

    for item in data["items"]:
        frame_id = item['id']
        frame_id = str(int(frame_id.split('_')[1]) + 1)

        obj_list = item["annotations"]

        for obj in obj_list: 
            track_id = obj["attributes"]["track_id"]
            group_id = obj["group"]

            bbox = obj["bbox"]

            view_id = get_view_id(bbox=bbox)

            bbox = get_original_coordinate(bbox, view_id)

            # append id to corresponding group
            if group_id not in groups: 
                groups[group_id] = [track_id]   
            else:
                if track_id not in groups[group_id]:
                    groups[group_id].append(track_id)

            obj_info = [frame_id, str(track_id), bbox[0], bbox[1], bbox[2], 
                        bbox[3], 1, 1, 1]

            view_objects["view_{}".format(view_id)].append(obj_info)

    # get global id for each object by mapping each id in group to its 
    # index in list 

    for view in view_objects:
        view_objects[view] = get_global_id(view_objects[view], groups)
        # print(view_objects)
        # exit()

    return view_objects, groups

def merge_gt_to_mot_gt(merge_gt, output_dir):
    view_objects, id_groups = get_view_objects(merge_gt=merge_gt)

    # for view in view_objects:
    #     print(view)
    #     for obj in view_objects[view]:
    #         print(obj)

    mkdir_if_missing(output_dir)

    for view in view_objects:
        save_path = osp.join(output_dir, "{}.txt".format(view))

        with open(save_path, 'w') as f:
            for obj in view_objects[view]:
                f.write("{},{},{},{},{},{},{},{},{}\n".format(obj[0], obj[1], 
                                                              obj[2], obj[3], 
                                                              obj[4], obj[5],
                                                              obj[6], obj[7], 
                                                              obj[8]))

    
merge_gt_to_mot_gt(merge_gt=args.merge_gt, output_dir='test_gt')