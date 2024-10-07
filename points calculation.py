import csv, os, json

""""

RCAT Points Calculation

V 0 . 3 . 4
on github

ALL CALCULATIONS ARE IN LBS AND sec

"""

"""
3 missions, ground ops, and report scores

mission one is just completion for 1 point
"""

with open('./settings.json','r') as jsonf:
    settings = json.load(jsonf)

def points_mission2(team_fuel, team_time, max_fueltime): # i know it doesnt have to be a function but it just makes me happier
    team_fueltime = team_fuel/team_time
    mission2 = 1 + (team_fueltime/max_fueltime)
    if mission2 > 2:
        return 2
    return float(mission2)

def points_mission3(team_laps,team_boxscore,team_weight,max_score): # team_XXX are self explanitory, max_score is max_(laps + fuel weight/time). This is not the max fuel divided by max time, this the best performing team in terms of (laps + fuel weight/time)
    try:
        mission3 = 2 + (team_laps+(team_boxscore/team_weight))/max_score
    except ZeroDivisionError:
        mission3=2+(team_laps/max_score)
    if mission3 > 3:
        return 3
    return mission3

def all_mission_calc(fuel_weight,highest_mission_achieved,m2_time=2.5,max_m2=0.5555,x1_weight=0.055,m3_laps=1,m3_boxscore=1,max_m3=1):
    points = 0
    if highest_mission_achieved>=1:
        points = 1
        if highest_mission_achieved>=2:
            points+=points_mission2(fuel_weight,m2_time,max_m2) # REPLACE LATER
            if highest_mission_achieved==3:
                points+=points_mission3(m3_laps,m3_boxscore,x1_weight,max_m3) # REPLACE

    elif ((highest_mission_achieved>3) or (highest_mission_achieved<0) or (type(highest_mission_achieved)!=int)):
        raise ValueError('highest_mission_achieved value must be 0, 1, 2, or 3.')
    return points

"""
This is where we start analyzing the possibilities using iteration.

Given all this cope, the first function will just handle writing this data to a csv (or xlsx if I'm feeling out there) so I can log data in an iteration format.
We are also assuming we complete all 3 missions (we arent going to win if we dont)
"""

set_list = [["IV","DV","C","Other"]] # This list will hold other lists. Think of a matrix. First index is row, second is column. ie set_list[row][column]

filename = ''

def find_filename(): #ive written this function too many times but I can't be bothered to copy/paste, it just changes the number so we dont overwrite previous files
    global filename
    files = os.listdir('./datafiles/')
    top = 0
    for file in files:
        num = int(file.lstrip('datafile_').rstrip('.csv'))
        if num>top:
            top = num
    filename = f'./datafiles/datafile_{top+1}.csv'
    return filename

filename = find_filename()

def savetosheet(data,loc = './datafiles/overwrite_test.csv',writetype='w'): # writes matrix to a file
    global filename
    with open(loc,writetype) as file:
        writer = csv.writer(file)
        for row in data:
            writer.writerow(row)

def mission_2(max_vals):
    set_list.append(['','','',''])
    set_list.append(['TIME (SEC)','POINTS','FUEL WEIGHT (LBS)',f'M2_max is {max_vals}'])
    for fuelweight in range(2,45,2):
        for time in range(60,300,5):
            missionval = points_mission2(fuelweight,time/10,max_vals)
            if missionval != None:
                set_list.append([time,missionval,fuelweight,''])
    set_list.append(['','','',''])
    savetosheet(set_list,loc=filename)

def mission_3(max_vals):
    set_list.append(['','','',''])
    set_list.append(['WEIGHT (LBS)','POINTS','LAPS',f'M3_max is {max_vals}'])
    for i in range(1,3): #### IMPORTANT NOTE #### If we do not get any bonus points, we default to zero. 
        boxscore=i
        if i == 2:
            boxscore = 2.5
        for x1weight in range(55,500,1):
            for laps in range(1,10,1):        
                missionval3 = points_mission3(laps,x1weight/1000,boxscore,max_vals)
                if missionval3 != None:        
                    set_list.append([x1weight/1000,missionval3,laps,''])
    set_list.append(['','','',''])
    savetosheet(set_list,loc=filename)

### Test Cases ###
mission_2(settings['Maxes']['m2_max'])
mission_3(settings['Maxes']['m3_max'])
mission_2(settings['Maxes']['reasonable_m2'])
mission_3(settings['Maxes']['reasonable_m3'])
print('done')