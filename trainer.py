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

# SETUP TRAINING AND TESTING SETS
# THE TESTING SELECTION IS NOT YET USED
directoryList = "./test.txt"
imagePaths = list()
tags = list()

# To be used if integer classification is more convenient
# 0 -> 'photography', 1 -> 'traditional', 2 -> 'digitalart'


def enumerateTags(tag):
    if (tag == "photography"):
        return 2
    elif (tag == "traditional"):
        return 0
    return 1

def reverseTags(value):
    if (value == 0):
        return "traditional"
    elif (value == 2):
        return "photography"
    return "digitalart"

dataSet = open(directoryList, 'r').read().splitlines()
for d in dataSet:
    imagePaths.append(d.split(' ')[0])# enumerateTags(d.split(' ')[1])) )
    tags.append(int((d.split(' ')[1])))

# imageSet = [filename for filename in os.listdir(path) if filename[0] == 'p']

trainingSizeRatio = 0.7
testingSizeRatio = 1.0 - trainingSizeRatio

trainingSize = round(trainingSizeRatio * len(imagePaths))
testingSize = len(imagePaths) - trainingSize

# trainingSet = random.sample(imageSet, trainingSize)
indexRange = range(len(imagePaths))
trainingSelection = random.sample(indexRange, trainingSize)
testingSelection = [i for i in indexRange if i not in trainingSelection]
# testingSet = [f for f in imageSet if f not in trainingSet]

trainingImagePaths = [imagePaths[i] for i in trainingSelection]
testiongImagePaths = [imagePaths[i] for i in testingSelection]
trainingTags = [tags[i] for i in trainingSelection]
testingTags = [tags[i] for i in testingSelection]

#--- TESTING SEPARATION TO BE USED LATER

# Load path/class_id image file:
# dataset_file = pathToFile

# Build the preloader array, resize images to 512x512 if necessary
print("Initializing preloader")

# Change filter_channel to false to use png images as well
X, Y = image_preloader(directoryList, image_shape=(512, 512), mode='file', categorical_labels=True, normalize=True, filter_channel=True)
print("Finished preloading!")

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
network = input_data(shape=[None, 512, 512, 3], data_preprocessing=img_prep, data_augmentation=img_aug)

# Step 1: Convolution
network = conv_2d(network, 32, 3, activation='relu')

# Step 2: Max pooling
network = max_pool_2d(network, 2)

# Step 3: Convolution again
# network = conv_2d(network, 64, 3, activation='relu')

# Step 4: Convolution yet again
# network = conv_2d(network, 64, 3, activation='relu')

# Step 5: Max pooling again
# network = max_pool_2d(network, 2)

# Step 6: Fully-connected 512 node neural network
# network = fully_connected(network, 512, activation='relu')

# Step 7: Dropout – throw away some data randomly during training to prevent over-fitting
# network = dropout(network, 0.5)

# Step 8: Fully-connected neural network with 3 outputs
network = fully_connected(network, 3, activation='softmax')

# Tell tflearn how we want to train the network
network = regression(network, optimizer='adam', loss='categorical_crossentropy', learning_rate=0.001)

# Wrap the network in a model object
model = tflearn.DNN(network, tensorboard_verbose=0)

# Build neural network and train
model.fit(X, Y, n_epoch=10, shuffle=True, validation_set=(X, Y),
show_metric=True, batch_size=96,
snapshot_epoch=True,
run_id='image-tagger')

# model.save("image-tagger.tfl")
print("\nNetwork trained!\n")

counter = 0
for img in X:
    prediction = model.predict([img])
    print(tags[counter])
    print("Result is ", reverseTags(np.argmax(prediction[0])))
    counter += 1
