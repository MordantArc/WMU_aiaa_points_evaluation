import csv, os, json

""""

Western Michigan University AIAA RCAT Points Calculation for 2024-2025 Competition

V 0 . 5 . 0

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
    if highest_mission_achieved>=1:                                                                             # in post (IE: in Excel or something). I'll leave it for the moment but I'll consider it non-functional
        points = 1
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

def find_filename():                                                                                            # ive written this function too many times but I can't be bothered to copy/paste, 
    global filename                                                                                             # it just changes the number of datafile so we dont overwrite previous files
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
    set_list.append(['','','',''])                                                                              # Spacer
    set_list.append(['TIME (SEC)','FUEL WEIGHT (LBS)','POINTS',f'M2 max value is set to {max_vals} ({name})'])

    fwsettings = settings["ranges"]["M2"]["fuelweight"]
    timesettings = settings["ranges"]["M2"]["time"]

    for fuelweight in range(fwsettings[0],fwsettings[1],fwsettings[2]):
        for time in range(timesettings[0],timesettings[1],timesettings[2]):

            missionval = points_mission2(fuelweight,time/10,max_vals)
            if missionval != None:                                                                              # This is old, I used to have it completely exclude mission values larger than what is possible
                set_list.append([time,fuelweight,missionval,''])                                                # Now it just adjusts it to the maximum and still includes it (IDK how I feel about keeping it)

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

def main():
    for max_name, max_values in settings['maxes'].items():
        if ('m2' in max_name):
            mission_2(max_values,name=max_name)
        elif ('m3' in max_name):
            mission_3(max_values,name=max_name)
        else:
            raise IndexError("Value found in 'Maxes' does not contain m2 or m3.")

### Test Cases ###
if __name__=="__main__":                                                                                        # I know we don't really need this but it makes me happy to have it so ¯\_(ツ)_/¯
    main()
    print('done')
