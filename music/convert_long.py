import os, csv, threading, subprocess, sys

tempo = 96


def write_music(music1, length):
    return '''0, 0, Header, 1, 2, 480
1, 0, Start_track
1, 0, Title_t, "Test"
1, 0, Time_signature, 3, 3, 96, 8
1, 0, Tempo, 300000
1, 0, End_track
2, 0, Start_track
2, 0, Instrument_name_t, "Church Organ"
2, 0, Program_c, 1, 19
'''+music1+'''2, '''+length+''', End_track
0, 0, End_of_file'''


def write_line(time, note, action):
    time_native = time * tempo
    note_num = ord(note)

    return ("2, "+str(time_native)+", "+action+", 0, "+str(note_num)+", 127")


def get_length(music1):
    a = music1[len(music1)-1]
    a = a.split(",")[1]
    return a


def run(file):
    print(file)
    with open(file, encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f)

        music = []
        output = []
        playing = ""

        for row in reader:
            music += row

        for time, notes in enumerate(music, start=1):
            for note in notes:
                if note in playing:
                    continue
                else:
                    output.append(write_line(time, note, "Note_on_c"))
                    playing += note

            for note in playing:
                if note not in notes:
                    playing = playing.replace(note, "")
                    output.append(write_line(time, note, "Note_off_c"))

        with open(""+file+"short", 'w') as myfile:
            music_str = ""
            for i in output:
                music_str += i+"\n"
            
            myfile.write(write_music(music_str, get_length(output)))
            name = myfile.name

            try:
                subprocess.call(["C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe", "csvmidi "+name+" "+name+".mid"])                
            except:
                os.system("csvmidi "+name+" "+name+".mid")


def start(files):
    for i in files:
        t = threading.Thread(target=run, args=(i,))
        t.start()


start(sys.argv[1:])