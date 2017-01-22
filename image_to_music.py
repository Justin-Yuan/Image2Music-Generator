# image_to_music.py
#
# Analyzes a given image and creates a song out of the contents
#
# Implements a drum-machine pattern consisting of bass (kick),
# snare and hi-hat sounds. It uses notes, three phrases, a part and
# a score, with each layer adding additional rhythms.
 
from music import *
import os,sys
import Image
import random

########## IMAGE ##########

#jpgfile = Image.open("cat_lying_on_grass.jpg")

#print jpgfile.bits, jpgfile.size, jpgfile.format

total_R = 2
total_G = 1
total_B = 1
chorus_R = 0
chorus_G = 1
chorus_B = 0

# The I for the chord progression
ch_Root = 0

# The chord progression

ch_progression = '.'

# Determine the root note
if total_R > total_G and total_R > total_B:
	ch_Root = 0
else:
	ch_Root = 1

# Determine the chord progression of the chorus
max_chorus_RGB = max([chorus_R, chorus_B, chorus_G])
if max_chorus_RGB == chorus_R:
	ch_progression = 'I V vi IV'
elif max_chorus_RGB == chorus_B:
	ch_progression == 'I vi IV V'
else:
	ch_progression == 'I V IV V'

########## MUSIC ##########

drumRepetitions = 8      # times to repeat drum pattern
rhythmGuitarRepetitions = 4
bassRepetitions = 16

##### define the data structure
score = Score("Image to Music", 96.0) # tempo is 96 bpm

rhythmGuitarPart = Part(OVERDRIVE_GUITAR, 0)

soloGuitarPart = Part(DISTORTION_GUITAR, 2)
soloGuitarPart.setDynamic(120)
bassPart = Part(ELECTRIC_BASS, 1)
drumsPart = Part("Drums", 0, 9)  # using MIDI channel 9 (percussion)

rhythmGuitarPhrase = Phrase(0.0)  	 # rhythm guitar phrases
soloGuitarPhrase = Phrase(0.0)	# solo guitar phrases
bassPhrase = Phrase(0.0)		 # bass phrases

bassDrumPhrase = Phrase(0.0)     # create phrase for each drum sound
snareDrumPhrase = Phrase(0.0)
hiHatPhrase = Phrase(0.0)

##### create musical data

### Guitar

## Chords

ch_A = [A4, E4, A5, CS5, E5]
ch_Am = [A4, E4, A5, C5, E5]
ch_AS = [A4 + 1, E4 + 1, A5 + 1, CS5 + 1, E5 + 1]
ch_ASm = [A4 + 1, E4 + 1, A5 + 1, C5 + 1, E5 + 1]
ch_B = [B4, FS4, B5, DS5, FS5]
ch_Bm = [B4, FS4, B5, D5, FS5]
ch_C = [C4, E4, G4, C5, E5]
ch_Cm = [C4, G4, C5, DS5, G5]
ch_CS = [C4 + 1, E4 + 1, G4 + 1, C5 + 1, E5 + 1]
ch_CSm = [C4 + 1, G4 + 1, C5 + 1, DS5 + 1, G5 + 1]
ch_D = [D4, A4, D5, FS5]
ch_Dm = [D4, A3, D5, F5]
ch_DS = [D4 + 1, A4 + 1, D5 + 1, FS5 + 1]
ch_DSm = [D4 + 1, A3 + 1, D5 + 1, F5 + 1]
ch_E = [E3, B4, E4, GS4, B5, E5]
ch_Em = [E3, B4, E4, G4, B5, E5]
ch_F = [F3, C4, F4, A5, F5]
ch_Fm = [F3, C4, F4, AS5, F5]
ch_FS = [F3 + 1, C4 + 1, F4 + 1, A5 + 1, F5 + 1]
ch_FSm = [F3 + 1, C4 + 1, F4 + 1, AS5 + 1, F5 + 1]
ch_G = [G3, B4, D4, G4, B5, G5]
ch_Gm = [G3, D4, G4, AS5, D5, G5]
ch_GS = [G3 + 1, B4 + 1, D4 + 1, G4 + 1, B5 + 1, G5 + 1]
ch_GSm = [G3 + 1, D4 + 1, G4 + 1, AS5 + 1, D5 + 1, G5 + 1]

# Dictionary for easy access to chords
ch_options = {
	0 : ch_A,
	1 : ch_Am,
	2 : ch_AS,
	3 : ch_ASm,
	4 : ch_B,
	5 : ch_Bm,
	6 : ch_C,
	7 : ch_Cm,
	8 : ch_CS,
	9 : ch_CSm,
	10 : ch_D,
	11 : ch_Dm,
	12 : ch_DS,
	13 : ch_DSm,
	14 : ch_E,
	15 : ch_Em,
	16 : ch_F,
	17 : ch_Fm,
	18 : ch_FS,
	19 : ch_FSm,
	20 : ch_G,
	21 : ch_Gm,
	22 : ch_GS,
	23 : ch_GSm
}

# Dictionary for chord progressions
ch_progression_options = {
	'I V vi IV' : [ch_Root, (ch_Root + 14) % 24, 
	(ch_Root + 19) % 24, (ch_Root + 10) % 24],

	'I vi IV V' : [ch_Root, (ch_Root + 19) % 24, 
	(ch_Root + 10) % 24, (ch_Root + 14) % 24],

	'I V IV V' : [ch_Root, (ch_Root + 14) % 24, 
	(ch_Root + 10) % 24, (ch_Root + 14) % 24]
}

# guitar chord progession I - V - vi - IV

guitar_Whole_Durations = [WN, WN, WN, WN]

# decide what the guitar chord progression is
rhythmGuitarPitches = [ ch_options[ch_progression_options[ch_progression][0]], ch_options[ch_progression_options[ch_progression][1]],
						ch_options[ch_progression_options[ch_progression][2]], ch_options[ch_progression_options[ch_progression][3]]]
rhythmGuitarDurations = guitar_Whole_Durations
rhythmGuitarPhrase.addNoteList(rhythmGuitarPitches, rhythmGuitarDurations)

# Solo guitar
s_Root = ch_progression_options[ch_progression][0] + 48
s_Scale = [0, 0, 0, 0, 0]
for i in range(len(s_Scale)):
	s_Scale[i] = PENTATONIC_SCALE[i]

for i in range(len(s_Scale)):
	s_Scale[i] = s_Root + s_Scale[i]

# picks a random note from the pentatonic scale
# pentatonic scale changes with the chord progression
soloGuitarPitches = [0] * 8 * 16
soloGuitarDurations = [EN] * 8 * 16
for i in range(len(soloGuitarDurations)):
	if i % 8 == 0 and i != 0:
		s_Root = ch_progression_options[ch_progression][(i // 8) % 4] + 48
		for j in range(len(s_Scale)):
			s_Scale[j] = PENTATONIC_SCALE[j]

		for j in range(len(s_Scale_Verse)):
			s_Scale[j] = s_Root + s_Scale[j]
		print(s_Scale)
	soloGuitarPitches[i] = random.choice(s_Scale)


soloGuitarPhrase.addNoteList(soloGuitarPitches, soloGuitarDurations)


### Bass G2 - D2 - E2 - C2
bassGuitarPitches = [0, 0, 0, 0]
for i in range(len(bassGuitarPitches)):
	bassGuitarPitches[i]   = ch_progression_options[ch_progression][i] // 2 + 12

# testing
# print(bassGuitarPitches)

bass_Quarter_Durations = [QN, QN, QN, QN]

# decide what the bass line is
bassPitches = bassGuitarPitches
bassDurations = bass_Quarter_Durations
bassPhrase.addNoteList(bassPitches, bassDurations)

### Drums

# bass drum pattern (one bass + one rest 1/4 note) x 4 = 2 measures
bassDrumPitches   = [BDR, REST] * 4
bassDrumDurations = [QN,  QN] * 4
bassDrumPhrase.addNoteList(bassDrumPitches, bassDrumDurations)
 
# snare drum pattern (one rest + one snare 1/4 note) x 4 = 2 measures
snarePitches   = [REST, SNR] * 4
snareDurations = [QN,   QN] * 4
snareDrumPhrase.addNoteList(snarePitches, snareDurations)
 
# hi-hat pattern (15 closed 1/8 notes + 1 open 1/8 note) = 2 measures
hiHatPitches   = [CHH] * 15 + [OHH]
hiHatDurations = [EN] * 15  + [EN]  
hiHatPhrase.addNoteList(hiHatPitches, hiHatDurations)
 
##### repeat material as needed
Mod.repeat(rhythmGuitarPhrase, rhythmGuitarRepetitions)
Mod.repeat(bassPhrase, bassRepetitions)
Mod.repeat(bassDrumPhrase, drumRepetitions)
Mod.repeat(snareDrumPhrase, drumRepetitions)
Mod.repeat(hiHatPhrase, drumRepetitions)

##### combine musical material

rhythmGuitarPart.addPhrase(rhythmGuitarPhrase)
rhythmGuitarPart.setDynamic(50)
soloGuitarPart.addPhrase(soloGuitarPhrase)
soloGuitarPart.setDynamic(100)
bassPart.addPhrase(bassPhrase)
bassPart.setDynamic(80)
drumsPart.addPhrase(bassDrumPhrase)
drumsPart.addPhrase(snareDrumPhrase)
drumsPart.addPhrase(hiHatPhrase)
score.addPart(rhythmGuitarPart)
score.addPart(soloGuitarPart)
score.addPart(bassPart)
score.addPart(drumsPart)

 
##### write midi
#Play.midi(score)
Write.midi(score, "image_to_music.mid")