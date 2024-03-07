import simpleaudio as sa 
import time as time 
import random 
import pygame
from midiutil import MIDIFile

########## TODO ##########
# - GIVE INTENSITY MORE MEANING
# - GIVE DURATION MORE MEANING 
# - ADD SWING
# - BETERE PLAYBACK -> NU KLOPT TIME NIET HELEMAAL
# DOORNBURG
#PYGAME
#MUTEX -> Lock
#PYTHON -> APP

######### section for initialisation ##########
# time section
pygame.init()
# Initialize Pygame clock
clock = pygame.time.Clock()

########## section for variables ###########

#patterns, a 1 equals a trigger and a 0 equals a silence. 16th notes, 1 measure
kick_pattern = [1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0] 
snare_pattern = [0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0] 
hihat_pattern = [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0]

#dictionaries 

#samples:
kick = sa.WaveObject.from_wave_file("../samples/kick/kick1.wav")
snare = sa.WaveObject.from_wave_file("../samples/snare/snare1.wav")
hihat = sa.WaveObject.from_wave_file("../samples/hihat/hihat1.wav")

instruments = kick, snare, hihat

#samples
bpm = 80

########## section for functions ##########

# def apply_swing(notes, swing_amount):
#function for making events according to the timestamps and a random instrument from the instrument list, also give the instruments a midinote value for exporting midi
def event_maker(t_stamp, instrument, durations, midinote, intensities, sample):
    event_list = []
    for x in range(len(t_stamp)):
           event_list.append({'instrument': instrument, 'timestamp': t_stamp[x], 'duration': durations[x], 'midinote': midinote, 'intensities': intensities[x], 'sample': sample})
    
    event_list.reverse()
    return event_list

def pattern_to_timestamps(pattern, measures):
    ts_list = [] # empty list to store the timestamps
    notedur = 60000 / (bpm * 4) # duration of a 16th note
    pattern_length = len(pattern)
    
    for measure in range(measures):
        for note_index in range(pattern_length):
            if pattern[note_index] == 1:
                # Calculate timestamp by adding the current measure's start time
                ts = (measure * pattern_length * notedur) + (note_index * notedur)
                ts_list.append(ts)

    return ts_list


def pattern_to_intensity(pattern, measures):
    intensity_list = []
    inensity_min = 0.6 
    intensity_max = 0.8

    for _ in range(measures):
        for x in range(len(pattern)):
            if pattern[x] == 1:
                intensity_list.append(round(random.uniform(inensity_min, intensity_max), 2))

    return intensity_list


#section for converting ts to durations so i can export to midi later on 
def ts_to_dur(ts_list, bpm):
    # Correctly calculate measure length in milliseconds for a 4/4 measure
    notedur = 60000/(bpm*4) #duration of a 16th note
    measure_length_ms = notedur * 16 #duration of a measure 
    dur_list = []
    ts_list.reverse()
    
    for i in range(len(ts_list) - 1):
        dur_note = ts_list[i] - ts_list[i + 1]
        dur_list.append(dur_note)
    
    # Correctly calculate the duration of the last note based on the measure length in milliseconds
    last_note_duration = measure_length_ms - ts_list[0]
    dur_list.append(last_note_duration)
    dur_list.reverse()
    
    return dur_list



########## section for running the code ##########

kick_ts = pattern_to_timestamps(kick_pattern,4)
snare_ts = pattern_to_timestamps(snare_pattern,4)
hihat_ts = pattern_to_timestamps(hihat_pattern,4)

print("kick timestamps:", kick_ts)
print("snare timestamps:", snare_ts)
print("hihat timestamps:", hihat_ts)

kick_dur = ts_to_dur(kick_ts,bpm)
snare_dur = ts_to_dur(snare_ts,bpm)
hihat_dur = ts_to_dur(hihat_ts,bpm)

print("kick durations:", kick_dur)
print("snare durations:", snare_dur)
print("hihat durations:", hihat_dur)

kick_intensities = pattern_to_intensity(kick_pattern,4)
snare_intensities = pattern_to_intensity(snare_pattern,4)
hihat_intensities = pattern_to_intensity(hihat_pattern,4)

print("kick intesities:", kick_intensities)
print("snare intesities:", snare_intensities)
print("hihat intesities:", hihat_intensities)

kick_events = event_maker(kick_ts, "kick", kick_dur, 40, kick_intensities, kick)
snare_events = event_maker(snare_ts, "snare", snare_dur, 44, snare_intensities, snare)
hihat_events = event_maker(hihat_ts, "hihat", hihat_dur, 48, hihat_intensities, hihat)

print("kick events:", kick_events)
print("snare events:", snare_events)
print("hihat events:", hihat_events)

#adding all the events together and sorting them in the right order according to the timestamp value
all_events = kick_events + snare_events + hihat_events
all_events = sorted(all_events, key=lambda x: x['timestamp'])
print(all_events)


########## section for playback ###########  
#copy the eventlist so i can still use the events if the user wants to output MIDI
all_events_buffer = list(all_events)
#section of the code for the audio playback
start_time_ms = pygame.time.get_ticks()

#var for popping an event from the event_list
event = all_events.pop(0)

#while loop for playing the sequence 
while True:
    #var for storing current time 
    current_time_ms = pygame.time.get_ticks()
    #check if the event has to be played
    if(current_time_ms - start_time_ms >= event['timestamp']):
        event['sample'].play()
        #replace the event var with the next event in the list and check if there are events left in the event_list
        if(all_events):
            event = all_events.pop(0)
        #if there are no events left in the list break the loop
        else:
            break

    else:
        pygame.time.wait(1)

pygame.time.wait(1000)