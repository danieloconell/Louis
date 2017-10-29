import shutil, os, csv, pprint

# move files out of folders
folders = os.listdir()
folders.remove('store.py')
for folder in folders:
    items = os.listdir(folder)
    for item in items:
        if item.split(".")[1] == 'mid':
            shutil.copy(folder+"/"+item, os.getcwd())

# Use midi to csv to change format
for file in files:
    outfile = file.rstrip(".mid")
    print(file)
    os.system("midicsv "+file+" ./csv/"+outfile+".csv")
