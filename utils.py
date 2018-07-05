''' Useful utility functions '''

import glob
import os

''' CONSTANTS '''

# Numeric class ids
TRADITIONAL_CLASS = 0
DIGITAL_CLASS = 1
PHOTOGRAPHY_CLASS = 2

# File name prefixes used for distinguishing digital vs traditional vs phtography
DIGITAL_PREFIX = "digitalart"
TRADITIONAL_PREFIX = "traditional"
PHOTOGRAPHY_PREFIX = "photography"

# dataset path id file - tflearn and tensorflow uses this file to load image data
PATH_ID_FILE_NAME = "dataset_path_id.txt"

# Directory where images are (relative path)
IMG_DIR = "images"

''' END CONSTANTS '''

def create_img_directory_list(img_list, use_absolute_paths=False):
    '''
    Creates a text file of the form /path/to/img1 class_id
    Input = list of all images (relative paths of the form a/b/c)
    print ("Hello There")
    '''
    with open(PATH_ID_FILE_NAME, 'w') as info_file:
        for img_name in img_list:
            class_id = TRADITIONAL_CLASS
            if DIGITAL_PREFIX in img_name:
                class_id = DIGITAL_CLASS
            elif PHOTOGRAPHY_PREFIX in img_name:
                class_id = PHOTOGRAPHY_CLASS
            file_path = img_name
            if use_absolute_paths:
                file_path = os.getcwd() + "/" + file_path
            info_file.write(file_path + " ")
            info_file.write(str(class_id))
            info_file.write("\n")


def fetch_img_list(img_directory, img_types=("*.jpg", "*.png")):
    # Fetch list of images of specified type
    if not img_directory.endswith("/"):
        img_directory += "/"

    img_list = []
    for img_type in img_types:
        img_list.extend(glob.glob(img_directory + img_type))
    return img_list

