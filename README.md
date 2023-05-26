#   **YOLO-DATASET-LABEL**

##  *INTRODUCTION*
This is a script to prepare dataset for yolo training. Using labelImg and labelme to label images, and labelImg is for boxes label, labelme is for polygons label.

##  *DIRS IN THE SCRIPT*
*   **Annotations_labelImg:**
dir to save labelImg labels

*   **Annotations_labelme:**
dir to save labelme labels

*   **data4use:**
dir to final data for use

*   **images:**
dir to save renamed images if necessary

*   **img:**
dir to source images

*   **scripts:**
dir to scripts

*   **targets:**
dir to merged labels

*   **predefined_class.txt:**
predefined classes

##  *HOW TO USE THIS SCRIPT*
1.  Use [rename_batch.py](scripts/rename_batch.py) to rename images in the img file 
2.  Use [img_generate.py](scripts/img_generate.py) to generate more images, include brightness change, contrast enhance, rotation, flip, add gaussian noise, add gaussian blur.
3.  Use labelImg and labelme to label images in the images file.
```
# use labelImg to label images, 'images' is the path of images, 'predefined_class.txt' is the classes to be labeled. 
$   labelImg images predefined_class.txt
#   use labelme to label images, 'images' is the path of images, 'predefined_class.txt' is the classes to be labeled. 
$   labelme images --labels predefined_class.txt
``` 
4.  Use [label2poly_yolo_format.py](scripts/label2poly_yolo_format.py) to hemerge box's and polygon's label. The final output is in the data4use folder.



