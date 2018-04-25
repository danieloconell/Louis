import os, sys, threading
import convert_long
import convert_short


def to_csv():
    a = []
    for file in folder:
        try:
            if file.split(".")[1] != "mid" and file.split(".")[1] != "midi":
                print(file)
        
                continue
        except:
            continue
        # midi to long csv
        print(file)
        outfile = file.split(".")[0]
        os.system("midicsv "+location+"/"+file+" "+outfile+".csv")

        files = os.listdir(location)
        for file in files:
            if len(file.split(".csv")) == 2:
                a.append(file)
        
        # long csv to short csv
        print(a)
        convert_short.start(a)


def to_midi():
    a = []
    for file in folder:
        try:
            if file.split(".")[1] == "csv":
                a.append(file)
        except:
            continue
        
        convert_long.start(a)


action = sys.argv[1].lower()
location = sys.argv[2]

folder = os.listdir(location)

if action == "csv":
    to_csv()
elif action == 'midi':
    to_midi()
else:
    print("usage: convert.py [action] [folder]")
