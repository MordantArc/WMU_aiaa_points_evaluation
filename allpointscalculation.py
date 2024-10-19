import csv, os, json

""""

Western Michigan University AIAA RCAT Points Calculation for 2024-2025 Competition

V 0 . 5 . 1

ALL CALCULATIONS ARE IN LBS AND sec

3 missions, ground ops, and report scores

mission one is just a completion score so it is not included as a function.
"""

with open('./settings.json','r') as jsonf:                                                                      # Loads the settings.JSON as a python dict
    settings = json.load(jsonf)

def points_mission2(team_fuel, team_time, max_fueltime):                                                        # i know it doesnt have to be a function but it just makes me happier
    team_fueltime = team_fuel/team_time
    mission2 = 1 + (team_fueltime/max_fueltime)
    if mission2 > 2:                                                                                            # A value that is higher than 2 means that our (fuelweight/time) was higher than the max (which is impossible) 
        return 2                                                                                                # This means our score gets used as a max, meaning we divide our score by our score - or just 1 point + the 1 completion point for 2 total.
    return float(mission2)

def points_mission3(team_laps,team_boxscore,team_weight,max_score):                                             # team_XXX are self explanitory, max_score is max_(laps + x1weight/time). 
    try:                                                                                                        # This is not the max fuel divided by max time, this the best performing team in terms of (laps + fuel weight/time)
        mission3 = 2 + (team_laps+(team_boxscore/team_weight))/max_score
    except ZeroDivisionError:
        mission3=2+(team_laps/max_score)
    if mission3 > 3:                                                                                            # same max rule as M2, it is impossible to get a score better than 3 for M3
        return 3                                                                                                
    return mission3

def all_mission_calc(fuel_weight,highest_mission_achieved,m2_time=2.5,max_m2=0.5555,x1_weight=0.055,m3_laps=1,m3_boxscore=1,max_m3=1):
    points = 0                                                                                                  # I havent used this function at all, I don't really know if it would be useful or if it's better to just combine it all
    if highest_mission_achieved>=1:                                                                             # in post (IE: in Excel or something). I'll leave it for the moment but I'll consider it non-functional because
        points = 1                                                                                              # I haven't verified that it works properly (I used it for like v0.2.0 or smth and now we're on v0.5.1 at the time of writing)
        if highest_mission_achieved>=2:
            points+=points_mission2(fuel_weight,m2_time,max_m2)
            if highest_mission_achieved==3:
                points+=points_mission3(m3_laps,m3_boxscore,x1_weight,max_m3)

    elif ((highest_mission_achieved>3) or (highest_mission_achieved<0) or (type(highest_mission_achieved)!=int)):
        raise ValueError('highest_mission_achieved value must be 0, 1, 2, or 3.')
    return points

"""
Right now this is all assuming CSV, and I think I'll keep it as is for now. XLSX is easier to use in Excel but CSVs work good enough.

We are also assuming we complete all 3 missions (we arent going to win if we dont)
"""

set_list = [["IV","C","DV","Other"]]                                                                            # This list will hold other lists. Think of a matrix. First index is row, second is column. ie set_list[row][column]

filename = ''

def find_filename():                                                                                            # 
    global filename                                                                                             # find_filename() just changes the number of datafile so we dont overwrite previous files
    try:                                                                                                        #
        files = os.listdir('./datafiles/')                                                                      # What I haven't tested is if there isn't any datafile in the folder. 
    except FileNotFoundError:                                                                                   # I know that it will create a folder if there isn't one, but I don't know how it
        os.mkdir('./datafiles/')                                                                                # will handle no datafile. I'm curious if it throws an error or if it just starts
        filename = './datafiles/datafile_1.csv'                                                                 # with 1. I'm avoiding this by manually setting the filename to datafile_1.csv
    top = 0 
    for file in files:
        num = int(file.lstrip('datafile_').rstrip('.csv'))
        if num>top:
            top = num
    filename = f'./datafiles/datafile_{top+1}.csv'
    return filename

filename = find_filename()

def savetosheet(data,loc = './datafiles/overwrite_test.csv',writetype='w'):                                     # writes matrix to a CSV file
    global filename
    with open(loc,writetype) as file:
        writer = csv.writer(file)
        for row in data:
            writer.writerow(row)

def mission_2(max_vals,name=""):
    set_list.append(['','','',''])
    set_list.append(['TIME (SEC)','FUEL WEIGHT (LBS)','POINTS',f'M2 max value is set to {max_vals} ({name})'])

    fwsettings = settings["ranges"]["M2"]["fuelweight"]
    timesettings = settings["ranges"]["M2"]["time"]

    for fuelweight in range(fwsettings[0],fwsettings[1],fwsettings[2]):
        for time in range(timesettings[0],timesettings[1],timesettings[2]):

            missionval = points_mission2(fuelweight,time,max_vals)
            if missionval != None:                                                                              # This is old, I used to have it completely exclude mission values larger than what is possible
                set_list.append([time,fuelweight,missionval,''])                                                # Now it just adjusts it to the maximum and still includes it (IDK how I feel about keeping 
                                                                                                                # these values instead of omitting them)
    set_list.append(['','','',''])
    savetosheet(set_list,loc=filename)

def mission_3(max_vals,name=""):
    set_list.append(['','','',''])
    set_list.append(['WEIGHT (LBS)','LAPS','POINTS',f'M3 max value is set to {max_vals} ({name})'])

    x1settings = settings["ranges"]["M3"]["x1weight"]
    lapsettings = settings["ranges"]["M3"]["laps"]

    for i in range(0,3):
        boxscore=i
        if i == 2:
            boxscore = 2.5
        for x1weight in range(x1settings[0],x1settings[1],x1settings[2]):
            for laps in range(lapsettings[0],lapsettings[1],lapsettings[2]):
                missionval3 = points_mission3(laps,x1weight/1000,boxscore,max_vals)
                if missionval3 != None:        
                    set_list.append([x1weight/1000,laps,missionval3,f'BOXSCORE : ({boxscore})'])
    set_list.append(['','','',''])
    savetosheet(set_list,loc=filename)

def query_all_missions():  
    print('This function is not in use.')                                                                       # This is just a function that uses the terminal to query a point score using a specific set of values.
    pass                                                                                                        # In english, this means we can enter things like fuel weight for our prototypes and get 
    while True:                                                                                                 # an expected score back. This makes it so that we don't have to fish for a score in the CSV
        resp = int(input('What is the highest mission attained? \n Must Be 1, 2, or 3.\nMission: '))            #
        if (resp>=1) and (resp<=3) and (type(resp)==int):                                                       # Personally I think this is all more trouble than it is worth, but I'm doing it anyway
            break                                                                                               # 
        else:
            print('Value must be 1, 2, or 3. Type the number, do not write out "Three"\n\n')
    
    fwsettings = settings["ranges"]["M2"]["fuelweight"]
    timesettings = settings["ranges"]["M2"]["time"]

    x1settings = settings["ranges"]["M3"]["x1weight"]
    lapsettings = settings["ranges"]["M3"]["laps"]

    if resp == 1:
        print('Mission 1 is only for a single completion point. If we only finished M1, we have 1 point.')
    else:
        points = 0
        while True:
            m2_fw = int(input("What is the Fuel Weight (in Lbs) for Mission 2?\nFuel Weight: "))
            if (m2_fw >=fwsettings[0]) and (m2_fw<=fwsettings[1]):
                break
            else:
                print(f'\n-- Fuel weight must be an integer between {fwsettings[0]} lbs and {fwsettings[1]} lbs. --\n')
        
        while True:
            m2_time = int(input("How fast (in seconds) did we complete Mission 2?\nSeconds: "))
            if (m2_time>=timesettings[0]) and (m2_time<=timesettings[1]):
                break
            else:
                print(f'\n-- Time must be an integer between {fwsettings[0]} sec and {fwsettings[1]} sec. --\n')
        
        m2_max_value = settings['maxes']['m2_max']                                                              # This needs to be changed to an input to ask what max value they want (the actual maxes vs reasonable maxes)

        points += points_mission2(m2_fw,m2_time,m2_max_value)                                                   # 
        if resp == 3:                                                                                           # The else here means completion of mission 3.
            pass


def main():
    for max_name, max_values in settings['maxes'].items():                                                      # This allows for multiple max values in settings.json 
        if ('m2' in max_name):                                                                                  # In practice this makes it easier to have the worst case maxes as well as the reasonable
            mission_2(max_values,name=max_name)                                                                 # maxes in settings and just iterate over all of them using this for loop
        elif ('m3' in max_name):
            mission_3(max_values,name=max_name)
        else:
            raise IndexError("Value found in 'Maxes' does not contain 'm2' or 'm3'.")

### Test Cases ###
if __name__=="__main__":                                                                                        # I know we don't really need this but it makes me happy to have it so ¯\_(ツ)_/¯
    main()
    print('done')