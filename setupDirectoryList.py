import csv
from os import listdir

fileName = "images-jpg.txt"
fileIn = "data.csv"

newFile = open(fileName, 'w')

files = sorted(listdir("./images-cropped/"))

for f in files:
    tag = 0
    if (f[0] == 't'):
        tag = 1
    elif (f[0] == 'd'):
        tag = 2
    newFile.write('./images/' + f + ' ' + tag + '\n')

newFile.close()

# with open(fileIn) as data:
  #   reader = csv.DictReader(data)
  #   info = [line for line in data]
