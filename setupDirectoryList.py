from os import listdir

fileName = "images-jpg.txt"
path = "./images-cropped/"

newFile = open(fileName, 'w')

files = sorted(listdir(path))
files = [f for f in files if 'jpg' not in f]

for f in files:
    tag = 0
    if (f[0] == 't'):
        tag = 1
    elif (f[0] == 'd'):
        tag = 2
    newFile.write('./images_jpg/' + f + ' ' + tag + '\n')

newFile.close()

# with open(fileIn) as data:
  #   reader = csv.DictReader(data)
  #   info = [line for line in data]
