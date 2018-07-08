from os import listdir
from random import shuffle

def randomizeImages():

    fileName = "images-jpgTrain.txt"
    directoryPath = './images/'

    newFile = open(fileName, 'w')

    files = sorted(listdir(directoryPath))
    files = [f for f in files if f[-4:] == '.jpg']

    files = [f for f in files if 'digitalart' not in f]
    shuffle(files)

    trainingSizeRatio = 0.7
    testingSizeRatio = 1.0 - trainingSizeRatio

    trainingSize = round(trainingSizeRatio * len(files))
    testingSize = len(files) - trainingSize

    trainingSelection = files[0:trainingSize]
    testingSelection = files[trainingSize:len(files)]


    for f in trainingSelection:
        tag = 0
        if (f[0] == 't'):
            tag = 1
        elif (f[0] == 'd'):
            tag = 2
        newFile.write(directoryPath + f + ' ' + str(tag) + '\n')

    newFile.close()

    newFile = open("images-jpgTest.txt", 'w')

    for f in testingSelection:
        tag = 0
        if (f[0] == 't'):
            tag = 1
        elif (f[0] == 'd'):
            tag = 2
        newFile.write(directoryPath + f + ' ' + str(tag) + '\n')

    newFile.close()

if __name__ == '__main__':
    randomizeImages()
