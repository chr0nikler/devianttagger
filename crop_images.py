import os
import glob
from PIL import Image, ImageOps

def fetch_img_list(img_directory, img_types=("*.jpg", "*.png")):
    # Fetch list of images of specified type
    img_list = []
    for img_type in img_types:
        img_list.extend(glob.glob(img_directory + img_type))
    return img_list

def crop_images(file_list, dest_directory, crop_dims=(512, 512)):
    # Crops image to desired size
    if not os.path.exists(dest_directory):
        os.makedirs(dest_directory)

    for file in file_list:
        _, filename = os.path.split(file)
        with Image.open(file) as image:
            cropped_img = ImageOps.fit(image, crop_dims, Image.ANTIALIAS)
            cropped_img.save(dest_directory + filename)
            cropped_img.close()


# Note this script should be run from one level above the images directory
# At least, that's where I ran and tested it
crop_img_directory = "./images-cropped/"
img_directory = "./images/"
img_list = fetch_img_list(img_directory)
crop_images(img_list, crop_img_directory)
#crop_images(img_list, crop_img_directory, (320, 320))
