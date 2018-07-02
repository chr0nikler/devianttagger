import csv
import urllib.request

with open("data.csv") as data:
    reader = csv.DictReader(data)
    data = [link for link in reader]
    links = [d['image'] for d in data]
    tags = [d['tag'] for d in data]

    # naming the files
    countPhoto = 0;
    countTraditional = 0;
    countDigital = 0;
    for dataPair in data:
        extension = dataPair['image'][-4:]
        if (extension == ".gif"):
            continue
        tagName = dataPair['tag']
        filename = tagName
        if (tagName == "traditional"):
            filename += str(countTraditional)
            countTraditional += 1
        elif (tagName == "digitalart"):
            filename += str(countDigital)
            countDigital += 1
        else:
            filename += str(countPhoto)
            countPhoto += 1
        filename += extension
        urllib.request.urlretrieve(dataPair['image'], "./images/" + filename)
        print(filename)


