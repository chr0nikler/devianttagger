# This script creates the required text file tat tflearn uses for reading in the image data

import utils
from utils import create_img_directory_list, fetch_img_list

img_list = fetch_img_list(utils.IMG_DIR)
create_img_directory_list(img_list)
# create_img_directory_list(img_list, True) #Create info file with abs file paths

