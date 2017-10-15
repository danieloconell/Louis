import shutil, os, csv, pprint

move files out of folders
folders = os.listdir()
folders.remove('store.py')
for folder in folders:
    items = os.listdir(folder)
    for item in items:
        if item.split(".")[1] == 'mid':
            shutil.copy(folder+"/"+item, os.getcwd())

Use midi to csv to change format
for file in files:
    outfile = file.rstrip(".mid")
    print(file)
    os.system("midicsv "+file+" ./csv/"+outfile+".csv")

# # Decrease size of csv files
# files = os.listdir()[:1]
# # files.remove('convert.py')
# # files.remove("midi")

# for file in files:
#     with open(file, encoding="utf-8", errors="replace") as f:
#         reader = csv.reader(f)
#         line_num = 0

#         # formatted_music = {}
#         # notes = ""
#         # start = False
#         # for row in reader:
#         #     line_num += 1

#         #     if row[2] == " Time_signature":
#         #         tempo = int(row[5])
#         #         start = True
#         #     if start:

#         #         time = round(int(row[1])/tempo)

#         #         if row[2] == " Note_on_c":
#         #             notes += chr(int(row[4]))

#         #         elif row[2] == " Note_off_c":
#         #                 notes.replace(chr(int(row[4])), "")

#         #         if time in formatted_music.keys():
#         #             formatted_music[time] += notes                 
#         #         else:
#         #             formatted_music[time] = notes
#                 # print(notes)
#         # pprint.pprint(formatted_music)