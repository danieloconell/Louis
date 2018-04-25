import os, csv

total_music = []
path = "data/sonata-beethoven/short"
folder = os.listdir(path)

for file in folder:
    print(file)
    with open(path+"/"+file) as f:
        reader = csv.reader(f)
        for row in reader:
            total_music = total_music + row

with open("data.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(total_music)
