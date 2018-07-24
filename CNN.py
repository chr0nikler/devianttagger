from __future__ import division, print_function, absolute_import
import random
import tensorflow as tf
import tflearn
from tflearn.data_utils import image_preloader
from tflearn.data_utils import shuffle
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.estimator import regression
from tflearn.data_preprocessing import ImagePreprocessing
from tflearn.data_augmentation import ImageAugmentation
import numpy as np
import scipy
import setupDirectoryList
from pathlib import Path

# SETUP DIRECTORY LIST
setupDirectoryList.randomizeImages()

# SETUP TRAINING AND TESTING SETS
# THE TESTING SELECTION IS NOT YET USED
directoryListTrain = "./images-jpgTrain.txt"
directoryListTest = "./images-jpgTest.txt"
imagePathsTrain = list()
imagePathsTest = list()
tags = list()

# To be used if integer classification is more convenient
# 2 -> 'photography', 0 -> 'traditional', 1 -> 'digitalart'

# note the tags in enumerateTags are not correct

dataSet = open(directoryListTrain, 'r').read().splitlines()
for d in dataSet:
    imagePathsTrain.append(d.split(' ')[0])
    tags.append(int((d.split(' ')[1])))

dataS = open(directoryListTest, 'r').read().splitlines()
for d in dataS:
    imagePathsTest.append(d.split(' ')[0])
# imageSet = [filename for filename in os.listdir(path) if filename[0] == 'p']

#--- TESTING SEPARATION TO BE USED LATER

# Load path/class_id image file:
# dataset_file = pathToFile

# Build the preloader array, resize images to 128x128 if necessary
print("Initializing preloader")

# Change filter_channel to false to use png images as well
X, Y = image_preloader(directoryListTrain, image_shape=(128, 128), mode='file', categorical_labels=True, normalize=True, filter_channel=True)
A, B = image_preloader(directoryListTest, image_shape=(128, 128), mode='file', categorical_labels=True, normalize=True, filter_channel=True)
print("Finished preloading 1!")

# Shuffle the data
# X, Y = shuffle(X, Y)

# Make sure the data is normalized
img_prep = ImagePreprocessing()
img_prep.add_featurewise_zero_center()
img_prep.add_featurewise_stdnorm()

# Create extra synthetic training data by flipping, rotating and blurring the
# images on our data set.
img_aug = ImageAugmentation()
img_aug.add_random_flip_leftright()
img_aug.add_random_rotation(max_angle=25.)
# img_aug.add_random_blur(sigma_max=3.)

# Input is a 32×32 image with 3 color channels (red, green and blue)
network = input_data(shape=[None, 128, 128, 3], data_preprocessing=img_prep, data_augmentation=img_aug)

# Step 1: Convolution
network = conv_2d(network, 32, 3, activation='relu')

# Step 2: Max pooling
network = max_pool_2d(network, 2)

# Step 3: Convolution again
network = conv_2d(network, 64, 3, activation='relu')

# Step 4: Convolution yet again
network = conv_2d(network, 64, 3, activation='relu')

# Step 5: Max pooling again
network = max_pool_2d(network, 2)

# More convolution layers
#network = conv_2d(network, 128, 3, activation='relu')
#network = conv_2d(network, 128, 3, activation='relu')

#network = max_pool_2d(network, 2)

# Step 6: Fully-connected 128 node neural network
network = fully_connected(network, 128, activation='relu')

# Step 7: Dropout – throw away some data randomly during training to prevent over-fitting
network = dropout(network, 0.6)

# Step 8: Fully-connected neural network with 3 outputs
network = fully_connected(network, 2, activation='softmax')

# Tell tflearn how we want to train the network
# categorical_crossentropy
network = regression(network, optimizer='adam', loss='categorical_crossentropy', learning_rate=0.001)

# Wrap the network in a model object
model = tflearn.DNN(network, tensorboard_verbose=3)

# Init graph
tflearn.config.init_graph() # by default, will use all available GPU memory

model_path = Path("./image-tagger.tfl.meta")
if model_path.is_file():
    print('here')
    model.load("./image-tagger.tfl")
else:
    # Build neural network and train
    print("Building Neural Network")
    model.fit(X, Y, n_epoch=50, shuffle=True, validation_set=(A, B),
    show_metric=True, batch_size=96,
    snapshot_epoch=True,
    run_id='image-tagger')

    model.save("image-tagger.tfl")
    print("\nNetwork trained!\n")

# New Accuracy Test
print("Starting accuracy test")
numerator = 0.0
for i in range(len(A)):
    prediction = model.predict([A[i]])
    predict_class = np.argmax(prediction)
    actual = np.argmax(B[i])
    if (predict_class == actual):
        numerator += 1

print("final accuracy is {0}".format(numerator / len(A)))
