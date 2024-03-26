import random
import mido
#THIS CODE IS BASED ON FAKE DATA, JUST TO DO SOME EXPERIMENTING 
#TODO:
#PERCENTAGE

######## VARIABLES ########
measure_amnt = 2
note_value = 16
grid_note_amnt = measure_amnt * note_value

input_rhythm_list = []
input_rhythm_amnt = 10
generated_rhythm = []

grid_prob_percentages = []

padnaam = "/Users/jellekraaijeveld/Documents/HKU1/Jaar_3/proj3/midi_data/test_grooves/3_hiphop_90_beat_4-4_1.midi"
midinote = 42

####### FUNCTIONS ########
def input_rhythms(rhythm_amnt, note_amnt): #FUNCTION FOR GENERATING FAKE INPUT RHYTHMS
    all_rhythms = []
    for _ in range(rhythm_amnt):
        single_rhythm = []
        for _ in range(note_amnt):
            single_rhythm.append(random.randint(0, 1))
        all_rhythms.append(single_rhythm)
    return all_rhythms

def calc_grid_probabilty(note_amnt, input_rhythms): #FUNCTION FOR CALCULATING THE PROBAILITY CHANCES
    rhythm_amnt = len(input_rhythms)
    rhythm_length = note_amnt
    on_list = []
    print(rhythm_amnt)
    for x in range(rhythm_length):
        on_amount = 0
        for y in range(rhythm_amnt):
            current_list = input_rhythms[y]
            on_or_of = current_list[x]
            if(on_or_of == 1):
                on_amount = on_amount + 1
        percentage = (on_amount/rhythm_amnt)*100
        on_list.append(percentage)
    return on_list
 
def new_rhythm(rhythm_percentages): #FUNCTION FOR GENERATING NEW RHYTHMS BASED ON THE PROBABILITY CHANCES
    rhythm = []

    for percentage in rhythm_percentages:
        random_nmbr = random.random()
        
        if random_nmbr < percentage / 100:
            rhythm.append(1)
        else:
            rhythm.append(0)
    
    return rhythm

def midi_to_binary(padnaam, midi_noot): #FUNCTION FOR TRANSLATING MIDIRHYTHMS TO BINARY RHYTHMS, FIRST QUANTIZES THE NOTES AND THEN SCANNING NOTE_ON'S
    mid = mido.MidiFile(padnaam)
    ticks_per_beat = mid.ticks_per_beat
    ticks_per_16e = ticks_per_beat / 4  # Aantal ticks per 16e noot

    # Bereken de totale duur van de MIDI in ticks om de lengte van de grid te bepalen
    totale_duratie_in_ticks = 0
    for track in mid.tracks:
        track_ticks = 0
        for msg in track:
            track_ticks += msg.time
        if track_ticks > totale_duratie_in_ticks:
            totale_duratie_in_ticks = track_ticks

    totale_16e_noten = round((totale_duratie_in_ticks / ticks_per_beat) * 4)  # Totale lengte in 16e noten
    grid = [0] * totale_16e_noten  # Initialiseer een grid van 16e noten met alle 'uit' (0)

    huidige_tijd_in_ticks = 0
    for track in mid.tracks:
        for msg in track:
            # Update de huidige tijd in ticks
            huidige_tijd_in_ticks += msg.time
            if msg.type == 'note_on' and msg.note == midi_noot and msg.velocity > 0:
                # Bepaal de positie in de grid van 16e noten, zonder -1 na de afronding
                positie = round(huidige_tijd_in_ticks / ticks_per_16e)
                if positie < len(grid):
                    grid[positie] = 1  # Markeer deze positie als 'aan' (1)

    return grid

def grid_shortener(grid, new_length): #FUNCTION FOR SHORTENING ALL THE GRIDS SO EVERYTHING IS EVENED OUT AND I HAVE USEABLE DATA
    # Splits de array in subarrays van 'lengte_subarray'
    subarrays = [grid[i:i + new_length] for i in range(0, len(grid), new_length)]
    # Behoud alleen subarrays die exact 'lengte_subarray' lang zijn
    subarrays = [subarray for subarray in subarrays if len(subarray) == new_length]
    return subarrays



def rhythms_to_probabilty():#FUNCTION FOR THE PROCESSING OF ALL THE MIDIFILES TO PROBABILITY CHANCES
    poop = 0
    return poop 

def midinotes_in_file(padnaam):
    mid = mido.MidiFile(padnaam)
    aanwezige_noten = set()  # Gebruik een set om dubbele noten te voorkomen

    for track in mid.tracks:
        for msg in track:
            if msg.type == 'note_on' and msg.velocity > 0:
                aanwezige_noten.add(msg.note)

    return sorted(list(aanwezige_noten))  # Sorteer de lijst voor gemakkelijke leesbaarheid


###### PROCESSING ########
# input_rhythm_list.extend(input_rhythms(input_rhythm_amnt, grid_note_amnt)) #EXTEND BECAUSE I WANT TO ADD THE ELEMENTS OF THE LIST AND NOT THE LIST AS AN ELEMENT
# print(input_rhythm_list)

# grid_prob_percentages = calc_grid_probabilty(grid_note_amnt, input_rhythm_list)
# print(grid_prob_percentages)

# generated_rhythm = new_rhythm(grid_prob_percentages)
# print(generated_rhythm)

grid = midi_to_binary(padnaam, midinote)
print(grid)

shortend_grids = grid_shortener(grid,grid_note_amnt)
# Print de subarrays om het resultaat te zien
for index, shortend_grid in enumerate(shortend_grids):
    print(f"Subarray {index+1}: {shortend_grid}")

notes = midinotes_in_file(padnaam)
print(f"Aanwezige MIDI noten: {notes}")


#PADNAAM: /Users/jellekraaijeveld/Documents/HKU1/Jaar_3/proj3/midi_data/test_grooves

    