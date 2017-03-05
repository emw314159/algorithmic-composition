
#
# useful libraries
#
import random
import midi
import sys
import math

#
# user settings
#
seed_to_use = 1
turnaround = 4
beats_per_minute = 120.
beats_per_measure = 4.
pulses_per_quarter_note__resolution = 100.
output_directory = 'output'
output_filename = 'randomly_generated_chord_progressions.mid'
N = 500

pitch_classes = [
    midi.C_2,
    midi.Db_2,
    midi.D_2,
    midi.Eb_2,
    midi.E_2,
    midi.F_2,
    midi.Gb_2,
    midi.G_2,
    midi.Ab_2,
    midi.A_2,
    midi.Bb_2,
    midi.B_2,
    ]

#
# for MIDI
#
ticks_per_beat = pulses_per_quarter_note__resolution
measure_time = beats_per_measure * ticks_per_beat

#
# start MIDI pattern
#
pattern = midi.Pattern(resolution=pulses_per_quarter_note__resolution)
track = midi.Track()
pattern.append(track)

#
# randomly generate material
#
random.seed(seed_to_use)
the_clock = 0.
current_measure = 1

for n in range(0, N):
    pitch_sample = [random.randint(0, 11) for x in range(0, turnaround)]
    intervals = [0]
    intervals.extend([x - y for x, y in zip(pitch_sample[1:], pitch_sample[0:-1])])

    current_pitch = random.randint(midi.C_4, midi.G_4)
    pitch_list = []
    for i in intervals:
        current_pitch += i
        pitch_list.append(current_pitch)

    print ','.join([';'.join([str(x) for x in intervals]), str(current_measure), ''])

    for n in range(0, 2):
        for note in pitch_list:

            on = midi.NoteOnEvent(tick=0, velocity=20, pitch=note)
            track.append(on)

            off = midi.NoteOffEvent(tick=int(measure_time), pitch=note)
            track.append(off)

    off = midi.NoteOffEvent(tick=2 * int(measure_time), pitch=note)
    track.append(off)

    current_measure += 10  # CRUDE




eot = midi.EndOfTrackEvent(tick=1)
track.append(eot)
midi.write_midifile(output_directory + '/' + output_filename, pattern)
