import os, csv, pprint, threading


def to_beats(time, tempo):
    return round(int(time)/tempo)


def to_char(num):
    return chr(int(num))


files = os.listdir()
files.remove('convert.py')
files.remove('mass_csv.py')
files.remove("midi")
files.remove("short")


def run(file):
    print(file)
    with open(file, encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f)

        music = []
        playing = ""
        for row in reader:
            if row[2] == " Time_signature":
                tempo = int(row[5])
                break

        f.seek(0)

        times = []
        for row in reader:
            times.append(to_beats(row[1], tempo))
        
        total_time = max(times)

        f.seek(0)

        for beat in range(0, total_time):
            for row in reader:
                if beat == to_beats(row[1], tempo):
                    if row[2] == " Note_on_c":
                        playing += to_char(row[4])

                    if row[2] == " Note_off_c":
                        playing = playing.replace(to_char(row[4]), "")

            music.append(playing)
            f.seek(0)

        with open("short/"+"short-"+file, 'w') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            wr.writerow(music)

    # pprint.pprint(music)


for i in files:
    t = threading.Thread(target=run, args=(i,))
    t.start()
