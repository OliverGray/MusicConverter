import midi
import math

pattern = midi.read_midifile("house_of_memories.mid")
# print pattern
# octave = track[0].data-1
notes = ['C', 'CS', 'D', 'DS', 'E', 'F', 'FS', 'G', 'GS', 'A', 'AS', 'B']
tracks = []
times = []
outfile = open('output.txt','w')

def convertNote(val):
    return 'NOTE_'+notes[(val%12)]+str(int(math.ceil(val/12))-1)


def trackNotes(track):
    curchord = []
    chords = []
    lastmajortick = 0

    for event in track:
        if type(event) is midi.NoteOnEvent:
            if event.tick == 0:
                curchord.append(convertNote(event.data[0])+','+str(lastmajortick))
            else:
                if event.tick > 50:
                    lastmajortick = (int(event.tick))
                chords.append(curchord)
                curchord = [convertNote(event.data[0])+','+str(lastmajortick)]

    return chords[::2]

def maxlen(chlist):
    max = 0
    for ch in chlist:
        if len(ch) > max:
            max = len(ch)

    return max

for section in pattern:
    trackdata = trackNotes(section)
    tracks.append([])
    times.append([])
    maxchord = maxlen(trackdata)
    for i in range(maxchord):
        tracks[-1].append('')
        times[-1].append([])

    for chord in trackdata:
        for x in range(maxchord):
            try:
                parts = chord[x].split(',')
                tracks[-1][x]+=parts[0]
                times[-1][x].append(int(parts[1]))
            except:
                tracks[-1][x] += ' '
                times[-1][x].append(times[-1][x-1][-1])

count = 0
for t in tracks:
    for line in t:
        count += 1
        outfile.write('Track '+str(count)+' Notes:"'+str(line)+'"\n')

count = 0
for n in times:
    for line in n:
        count += 1
        outfile.write('Track '+str(count)+' Timing:'+str(line)+'\n')
