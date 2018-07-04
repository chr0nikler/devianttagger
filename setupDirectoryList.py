import csv
from os import listdir

fileName = "imagePathsIds.txt"
fileIn = "data.csv"

newFile = open(fileName, 'w')

files = sorted(listdir("./images/"))
for f in files:
    tag = "photography"
    if (f[0] == 't'):
        tag = "traditional"
    elif (f[0] == 'd'):
        tag = "digitalart"
    newFile.write('./images/' + f + ' ' + tag + '\n')

newFile.close()

# with open(fileIn) as data:
  #   reader = csv.DictReader(data)
  #   info = [line for line in data]

