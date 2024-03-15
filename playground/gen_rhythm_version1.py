import random
#THIS CODE IS BASED ON FAKE DATA, JUST TO DO SOME EXPERIMENTING 
#TODO:
#PERCENTAGE

######## VARIABLES ########
measure_amnt = 2
note_value = 16
grid_note_amnt = measure_amnt * note_value

input_rhythm_list = []
input_rhythm_amnt = 10

grid_prob_percentages = []

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
        on_list.append(on_amount)
    return on_list

   
    


         
###### PROCESSING ########
input_rhythm_list.extend(input_rhythms(input_rhythm_amnt, grid_note_amnt)) #EXTEND BECAUSE I WANT TO ADD THE ELEMENTS OF THE LIST AND NOT THE LIST AS AN ELEMENT
print(input_rhythm_list)

print(calc_grid_probabilty(grid_note_amnt, input_rhythm_list))

# def rhythm_generator():
    