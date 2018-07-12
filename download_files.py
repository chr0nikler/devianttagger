import csv
import os
import urllib.request
import multiprocessing

directory = "./images"
if not os.path.exists(directory):
    os.makedirs(directory)
with open("data.csv") as data:
    reader = csv.DictReader(data)
    data = [link for link in reader]
    links = [d['image'] for d in data]
    tags = [d['tag'] for d in data]

    # naming the files
    countPhoto = [0]
    countTraditional = [0]
    countDigital = [0]
    countErrors = [0]

    def init(l):
        global lock
        lock = l

    def downloadImage(dataPair):
        try:
            extension = dataPair['image'][-4:]
            if ('jpg' not in extension):
                return
            tagName = dataPair['tag']
            filename = tagName
            if (tagName == "traditional"):
                #lock.acquire()
                filename += str(countTraditional[0])
                countTraditional[0] += 1
                #lock.release()
            elif (tagName == "digitalart"):
                filename += str(countDigital[0])
                countDigital[0] += 1
            else:
                filename += str(countPhoto[0])
                countPhoto[0] += 1
            filename += extension
            urllib.request.urlretrieve(dataPair['image'], "./images/" + filename)
            print(filename)
        except:
            tagName = dataPair['tag']
            if (tagName == "traditional"):
                countTraditional[0] -= 1
            elif (tagName == "digitalart"):
                countDigital[0] -= 1
            else:
                countPhoto[0] -= 1
            countErrors[0] += 1
            print(countErrors[0])

    #l = multiprocessing.Lock()
    #with multiprocessing.Pool(initializer=init, initargs=(l,)) as p:
        #p.map(downloadImage, data)
    for dataPair in data:
        downloadImage(dataPair)
