# A simple deploy for MTMC annotation post process 

## Run application locally: 

```bash
pip install -r requirements.txt
```

```bash
streamlit run app.py
```

There are 2 sections on the UI, which correspoding to: 

## Convert from list of single view MOT annotations to multiple view MOT annotation
Upload a zip of dictionary, which have the following structure:

```bash
root
  |
  |__view_1.txt
  |__view_2.txt
  |__view_3.txt
  |__view_4.txt
```

Where each `txt` file is the `gt.txt` file in MOT annotation format of that view

You can then download the zip file of MOT format:
```bash
gt
|
|__gt.txt
|__labels.txt
```

You can upload directly the downloaded zip file to CVAT for multiple view.

## Convert from multiple view annotation (Datumaru format) to list of single view MOT annotations

Upload a zip annotation in Datumaru format (download from CVAT). The output zip file have the following structure: 
```bash
root
  |
  |__view_1
  |     |__gt
  |     |   |__gt.txt
  |     |   |__labels.txt
  |     |
  |     |__gt.zip
  |
  |__view_2
  |     |__gt
  |     |   |__gt.txt
  |     |   |__labels.txt
  |     |
  |     |__gt.zip
  |
  |__view_3
  |     |__gt
  |     |   |__gt.txt
  |     |   |__labels.txt
  |     |
  |     |__gt.zip
  |
  |__view_4
        |__gt
        |   |__gt.txt
        |   |__labels.txt
        |
        |__gt.zip
```
