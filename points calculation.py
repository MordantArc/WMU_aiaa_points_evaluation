import csv, os

""""

RCAT Points Calculation

(wip)

ALL CALCULATIONS ARE IN LBS AND sec

"""

"""
3 missions, ground ops, and report scores

mission one is just completion for 1 point

mission two has this formula:
M2 = 1 + [N_(fuel weight / time) / Max_(fuel weight / time] , where Max_(fuel weight / time) is the highest (fuel weight / time) score of all teams. 

mission three:
M3 = 2 + [N_(# laps flown + (bonus box score / X-1 test vehicle weight)) / Max_(# laps flown + (bonus box score / X1 test vehicle weight)] , where Max_(# laps flown + (bonus box score / X-1 test vehicle weight) is the highest (# laps flown + (bonus box score / X-1 test vehicle weight) score of all teams.


"""

def points_mission2(team_fuel, team_time, max_fueltime): # i know it doesnt have to be a function but it just makes me happier
    team_fueltime = team_fuel/team_time
    mission2 = 1 + (team_fueltime/max_fueltime)
    return float(mission2)

def points_mission3(team_laps,team_boxscore,team_weight,max_score): # team_XXX are self explanitory, max_score is max_(laps + fuel weight/time). This is not the max fuel divided by max time, this the best performing team in terms of (laps + fuel weight/time)
    try:
        mission3 = 2 + (team_laps+(team_boxscore/team_weight))/max_score
    except ZeroDivisionError:
        mission3=2+(team_laps/max_score)
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

Mission 1 is the easiest, we either get a point or we dont. We're assuming that if we cannot complete a mission, all subsequent missions are also a failure.

For 2 and 3, each maximum value can be determined(within reason) letting us graph our data in multiple sets assuming the worst(as in other teams having the best score possible) and best (we have the highest score, which equates to a score of 2 for m2 and 3 for m3)



For M2
---
The denominator is just the highest value of (fuel/time). The maximum weight of an aircraft is 55 lbs. This means the theoretical maximum would be closer to 45-50 lbs for fuel as the aircraft will take around 5-10 lbs (minimum)
The longest time is about 5 minutes, but ideally we have the shortest time to complete 3 laps. We'll call it a minute thirty as a theoretical fastest model. We can work this back later as heavier aircraft may go slower.

This means (with a very generous set of scores) that a max value can start around 0.555. Keep in mind that for the best team with this score, this only nets them the max 1 point (team_fuelweight/max_fuelweight). It just makes everyone elses score lower



For M3
---
Theis one is more complicated, but I'll skim the explanation and give my estimates.
8 laps max 
best boxscore of 2.5
best weight of 25g, 0.055 lbs

this gives us a max score of (8+2.5/0.055) or 53.4545455. Again, this is not the actual score but the denominator. Max points on the flight portion is 3 (2 completion, 1 bonus points)






Given all this cope, the first function will just handle writing this data to a csv (or xlsx if I'm feeling out there) so I can log data in an iteration format.
We are also assuming we complete all 3 missions (we arent going to win if we dont)
"""
m2_max = 0.5555556
m3_max = 53.4545455


set_list = [["IV","DV","C","Other"]] # This list will hold other lists. Think of a matrix. First index is row, second is column. ie set_list[row][column]

def savetosheet(data,loc = './datafiles/overwrite_test.csv',writetype='w'): # writes matrix to a file
    with open(loc,writetype) as file:
        writer = csv.writer(file)
        for row in data:
            writer.writerow(row)

def find_filename(): #ive written this function too many times but I can't be bothered to copy/paste, it just changes the number so we dont overwrite previous files
    files = os.listdir('./datafiles/')
    top = 0
    for file in files:
        num = int(file.lstrip('datafile_').rstrip('.csv'))
        if num>top:
            top = num
    filename = f'./datafiles/datafile_{top+1}.csv'
    return filename

def mission_2():
    set_list.append(['','','',''])
    set_list.append(['TIME (SEC)','POINTS','FUEL WEIGHT (LBS)',f'M2_max is {m2_max}'])
    for fuelweight in range(2,45,2):
        for time in range(60,300,5):
            set_list.append([time,points_mission2(fuelweight,time/10,m2_max),fuelweight,''])
    set_list.append(['','','',''])
    savetosheet(set_list,loc=find_filename())

def mission_3():
    set_list.append(['','','',''])
    set_list.append(['WEIGHT (LBS)','POINTS','LAPS',f'M3_max is {m3_max}'])
    for i in range(1,3): #### IMPORTANT NOTE #### If we do not get any bonus points, we default to zero. 
        boxscore=i
        if i == 2:
            boxscore = 2.5
        for x1weight in range(55,550,1):
            for laps in range(1,10,1):                
                set_list.append([x1weight/1000,points_mission3(laps,x1weight/1000,boxscore,m3_max),laps,''])
    set_list.append(['','','',''])
    savetosheet(set_list,loc=find_filename())

### Test Cases ###
mission_2()
mission_3()
print('done')