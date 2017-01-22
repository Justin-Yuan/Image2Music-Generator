# image_to_music.py
#
# Analyzes a given image and creates a song out of the contents
#
# Implements a drum-machine pattern consisting of bass (kick),
# snare and hi-hat sounds. It uses notes, three phrases, a part and
# a score, with each layer adding additional rhythms.
 
from music import *
import os,sys


import random
import math

# Probability Function for melodic improvisation

def improv(avg_R, avg_G, avg_B, norm_R, norm_G, norm_B, i):
	total_RGB = avg_R + avg_G + avg_B
	sign = 1
	if total_RGB > (255 + 255 + 255) // 2:
		sign = -1
	chance_hit = (norm_R - norm_B) * 10 * sign * cos(i / 8 * math.pi)
	return chance_hit

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

ch_dict = {
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

# declare the variable I for the root of the chord progression
ch_Root = 0

# Dictionary for chord progressions

ch_prog_dict = {
	'I V IV V' : [ch_Root, (ch_Root + 14) % 24, 
	(ch_Root + 10) % 24, (ch_Root + 14) % 24],

	'I V vi IV' : [ch_Root, (ch_Root + 14) % 24, 
	(ch_Root + 19) % 24, (ch_Root + 10) % 24],

	'I vi IV V' : [ch_Root, (ch_Root + 19) % 24, 
	(ch_Root + 10) % 24, (ch_Root + 14) % 24],

	'vi I V II' : [(ch_Root + 19) % 24, ch_Root,
	(ch_Root + 14) % 24, (ch_Root + 4) % 24],

	'vi I iii iii' : [(ch_Root + 19) % 24, ch_Root,
	(ch_Root + 7) % 24, (ch_Root + 7) % 24]
}



chorusMeanColor = []

fp = open('chorusMeanColor.txt', 'rb')
for item in fp:
	chorusMeanColor.append(float(item))
fp.close()

# RGB array containing all RGB values of interest
rgb_array = chorusMeanColor

# declare variables to hold average of RGB values
avg_R = 0
avg_G = 0
avg_B = 0

# put average in those variables
n = 0
for i in range(len(rgb_array) // 3):
	n += 1
	avg_R += rgb_array[i * 3]
	avg_G += rgb_array[i * 3 + 1]
	avg_B += rgb_array[i * 3 + 2]

avg_R /= n
avg_G /= n
avg_B /= n	

# declare the variable I for the root of the chord progression
ch_Root = 0

# Determine the root note (even/major if large total RGB value, else minor)
ch_Root = random.randint(0, 24)
if avg_R + avg_G + avg_B > 255 * 1.5:
	if ch_Root % 2 != 0: # if odd
		ch_Root -= 1
else:
	if ch_Root % 2 == 0: # if even
		ch_Root -= 1

# declare the chord progression

ch_prog = '.'

# declare the total_RGB variable used for determining chord progression
total_RGB = avg_R + avg_G + avg_B

# the different chord progressions and their relation to total_RGB
ch_I_V_IV_V = 255 + 255 + 255
ch_I_V_vi_IV = ch_I_V_IV_V * 0.8
ch_I_vi_IV_V = ch_I_V_IV_V * 0.6
ch_vi_I_V_II = ch_I_V_IV_V * 0.4
ch_vi_I_iii_iii = ch_I_V_IV_V * 0.2

# calculate minimum difference
ch_I_V_IV_V = abs(ch_I_V_IV_V - total_RGB)
ch_I_V_vi_IV = abs(ch_I_V_vi_IV - total_RGB)
ch_I_vi_IV_V = abs(ch_I_vi_IV_V - total_RGB)
ch_vi_I_V_II = abs(ch_vi_I_V_II - total_RGB)
ch_vi_I_iii_iii = abs(ch_vi_I_iii_iii - total_RGB)

min_total_RGB_diff = min(ch_I_V_IV_V, ch_I_V_vi_IV,
				ch_I_vi_IV_V, ch_vi_I_V_II, ch_vi_I_iii_iii)

# finally determine the chord progression
if min_total_RGB_diff == ch_I_V_IV_V:
	ch_prog = 'I V IV V'
elif min_total_RGB_diff == ch_I_V_vi_IV:
	ch_prog = 'I V vi IV'
elif min_total_RGB_diff == ch_I_vi_IV_V:
	ch_prog = 'I vi IV V'
elif min_total_RGB_diff == ch_vi_I_V_II:
	ch_prog = 'vi I V II'
elif min_total_RGB_diff == ch_vi_I_iii_iii:
	ch_prog = 'vi I iii iii'

# declare variable for the melodic instrument
melody_instrument = 0

normalizer_RGB = max([avg_R, avg_G, avg_B])
norm_avg_RGB = [avg_R / normalizer_RGB,
				avg_G / normalizer_RGB,
				avg_B / normalizer_RGB]

# normalized vectors for selecting instruments

norm_Flute = [0, 1, 0.5]
norm_Dist_Guitar = [1, 0, 0.3]
norm_Piano = [0.3, 0.3, 1]
norm_Violin = [1, 1, 1]
norm_Sax = [0, 0, 1]

# calculate min distance between vectors

for i in range(3):
	norm_Flute[i] -= norm_avg_RGB[i]
	norm_Flute[i] = abs(norm_Flute[i])
	norm_Dist_Guitar[i] -= norm_avg_RGB[i]
	norm_Dist_Guitar[i] = abs(norm_Dist_Guitar[i])
	norm_Piano[i] -= norm_avg_RGB[i]
	norm_Piano[i] = abs(norm_Piano[i])
	norm_Violin[i] -= norm_avg_RGB[i]
	norm_Violin[i] = abs(norm_Violin[i])
	norm_Sax[i] -= norm_avg_RGB[i]
	norm_Sax[i] = abs(norm_Sax[i])

sum_Flute = sum(norm_Flute)
sum_Dist_Guitar = sum(norm_Dist_Guitar)
sum_Piano = sum(norm_Piano)
sum_Violin = sum(norm_Violin)
sum_Sax = sum(norm_Sax)

min_instr = min(sum_Flute, sum_Dist_Guitar, sum_Piano,
				sum_Violin, sum_Sax)

# determine which instrument plays the melody
if min_instr == sum_Flute:
	melody_instrument = FLUTE
elif min_instr == sum_Dist_Guitar:
	melody_instrument = DISTORTION_GUITAR
elif min_instr == sum_Piano:
	melody_instrument = PIANO
elif min_instr == sum_Violin:
	melody_instrument = VIOLIN
elif min_instr == sum_Sax:
	melody_instrument = SAXOPHONE

########## MUSIC ##########

drum_reps = 8      # times to repeat drum pattern
harmony_reps = 4
bass_reps = 16

# tempo is a variable bpm
tempo = random.randint(0, 3)
tempo_dict = { 0 : 80, 1 : 96, 2 : 108, 3 : 120}
tempo = tempo_dict[tempo]

##### define the data structure to store the score
score = Score("Image to Music", tempo) 

melody_part = Part(melody_instrument, 0)

harmony_part = Part(OVERDRIVE_GUITAR, 1)

bass_part = Part(ELECTRIC_BASS, 2)

drums_part = Part("Drums", 0, 9)  # using MIDI channel 9 (percussion)

melody_phrase = Phrase(0.0)	# melody phrases
harmony_phrase = Phrase(0.0)  	 # harmony phrases
bass_phrase = Phrase(0.0)		 # bass phrases

bass_drum_phrase = Phrase(0.0)     # create phrase for each drum sound
snare_drum_phrase = Phrase(0.0)
hi_hat_phrase = Phrase(0.0)

##### create musical data

### Harmony

# chord progession is determined previously in ch_prog

whole_4_durations = [WN, WN, WN, WN]

# 
harmony_pitches = [ ch_dict[ch_prog_dict[ch_prog][0]], ch_dict[ch_prog_dict[ch_prog][1]],
						ch_dict[ch_prog_dict[ch_prog][2]], ch_dict[ch_prog_dict[ch_prog][3]]]
harmony_durations = whole_4_durations
harmony_phrase.addNoteList(harmony_pitches, harmony_durations)

### Melody
m_Root = ch_prog_dict[ch_prog][0] + 48
m_Scale = [0, 0, 0, 0, 0]
for i in range(len(m_Scale)):
	m_Scale[i] = PENTATONIC_SCALE[i]

for i in range(len(m_Scale)):
	m_Scale[i] = m_Root + m_Scale[i]

# picks a random note from the pentatonic scale
# pentatonic scale changes with the chord progression
melody_pitches = [0] * 16 * 16
melody_durations = [SN] * 16 * 16
for i in range(len(melody_durations)):

	# change the pentatonic scale to follow the chord progression
	if i % 8 == 0 and i != 0:
		s_Root = ch_prog_dict[ch_prog][(i // 8) % 4] + 48
		for j in range(len(m_Scale)):
			m_Scale[j] = PENTATONIC_SCALE[j]

		for j in range(len(m_Scale)):
			m_Scale[j] = m_Root + m_Scale[j]
	
	# probabilities that a note will appear
	chance = random.randint(0, 100)
	hit = False
	if i % 16 == 0:
		hit = chance > 5
	elif (i - 1) % 16 == 0:
		hit = chance > 40 + improv(avg_R, avg_G, avg_B, norm_avg_RGB[0], norm_avg_RGB[1], norm_avg_RGB[2], i)
	elif (i - 2) % 16 == 0:
		hit = chance > 35 + improv(avg_R, avg_G, avg_B, norm_avg_RGB[0], norm_avg_RGB[1], norm_avg_RGB[2], i)
	elif (i - 3) % 16 == 0:
		hit = chance > 45 + improv(avg_R, avg_G, avg_B, norm_avg_RGB[0], norm_avg_RGB[1], norm_avg_RGB[2], i)
	elif (i - 4) % 16 == 0:
		hit = chance > 15
	elif (i - 5) % 16 == 0:
		hit = chance > 50 + improv(avg_R, avg_G, avg_B, norm_avg_RGB[0], norm_avg_RGB[1], norm_avg_RGB[2], i)
	elif (i - 6) % 16 == 0:
		hit = chance > 45 + improv(avg_R, avg_G, avg_B, norm_avg_RGB[0], norm_avg_RGB[1], norm_avg_RGB[2], i)
	elif (i - 7) % 16 == 0:
		hit = chance > 30 + improv(avg_R, avg_G, avg_B, norm_avg_RGB[0], norm_avg_RGB[1], norm_avg_RGB[2], i)
	elif (i - 8) % 16 == 0:
		hit = chance > 5
	elif (i - 9) % 16 == 0:
		hit = chance > 40 + improv(avg_R, avg_G, avg_B, norm_avg_RGB[0], norm_avg_RGB[1], norm_avg_RGB[2], i)
	elif (i - 10) % 16 == 0:
		hit = chance > 50 + improv(avg_R, avg_G, avg_B, norm_avg_RGB[0], norm_avg_RGB[1], norm_avg_RGB[2], i)
	elif (i - 11) % 16 == 0:
		hit = chance > 45 + improv(avg_R, avg_G, avg_B, norm_avg_RGB[0], norm_avg_RGB[1], norm_avg_RGB[2], i)
	elif (i - 12) % 16 == 0:
		hit = chance > 20 + improv(avg_R, avg_G, avg_B, norm_avg_RGB[0], norm_avg_RGB[1], norm_avg_RGB[2], i)
	elif (i - 13) % 16 == 0:
		hit = chance > 50 + improv(avg_R, avg_G, avg_B, norm_avg_RGB[0], norm_avg_RGB[1], norm_avg_RGB[2], i)
	elif (i - 14) % 16 == 0:
		hit = chance > 50 + improv(avg_R, avg_G, avg_B, norm_avg_RGB[0], norm_avg_RGB[1], norm_avg_RGB[2], i)
	elif (i - 15) % 16 == 0:
		hit = chance > 40 + improv(avg_R, avg_G, avg_B, norm_avg_RGB[0], norm_avg_RGB[1], norm_avg_RGB[2], i)
	# notes	
	if hit:
		melody_pitches[i] = random.choice(m_Scale)
	else:
		melody_pitches[i] = 0


melody_phrase.addNoteList(melody_pitches, melody_durations)

### Bass G2 - D2 - E2 - C2
bass_pitches = [0, 0, 0, 0]
for i in range(len(bass_pitches)):
	bass_pitches[i]   = ch_prog_dict[ch_prog][i] // 2 + 12

quarter_4_durations = [QN, QN, QN, QN]

# decide what the bass line is
bass_pitches = bass_pitches
bass_durations = quarter_4_durations
bass_phrase.addNoteList(bass_pitches, bass_durations)

### Drums

## Pattern 1

# bass drum pattern (one bass + one rest 1/4 note) x 4 = 2 measures
bass_drum_pitches   = [BDR, REST] * 4
bass_drum_durations = [QN,  QN] * 4
bass_drum_phrase.addNoteList(bass_drum_pitches, bass_drum_durations)
 
# snare drum pattern (one rest + one snare 1/4 note) x 4 = 2 measures
snare_pitches   = [REST, SNR] * 4
snare_durations = [QN,   QN] * 4
snare_drum_phrase.addNoteList(snare_pitches, snare_durations)
 
# hi-hat pattern (15 closed 1/8 notes + 1 open 1/8 note) = 2 measures
hi_hat_pitches   = [CHH] * 15 + [OHH]
hi_hat_durations = [EN] * 15  + [EN]  
hi_hat_phrase.addNoteList(hi_hat_pitches, hi_hat_durations)

## Pattern 2



##### repeat material as needed
Mod.repeat(harmony_phrase, harmony_reps)
Mod.repeat(bass_phrase, bass_reps)
Mod.repeat(bass_drum_phrase, drum_reps)
Mod.repeat(snare_drum_phrase, drum_reps)
Mod.repeat(hi_hat_phrase, drum_reps)

##### combine musical material

melody_part.addPhrase(melody_phrase)
melody_part.setDynamic(100)

harmony_part.addPhrase(harmony_phrase)
harmony_part.setDynamic(50)

bass_part.addPhrase(bass_phrase)
bass_part.setDynamic(80)

drums_part.addPhrase(bass_drum_phrase)
drums_part.addPhrase(snare_drum_phrase)
drums_part.addPhrase(hi_hat_phrase)

score.addPart(melody_part)
score.addPart(harmony_part)
score.addPart(bass_part)
score.addPart(drums_part)

 
##### write midi
Play.midi(score)
Write.midi(score, "image_to_music.mid")