# WMU AIAA Points Evaluation
Evaluates the possible points we can score in the 24-25 competition. This will aid in optimizing our entry in the competition.

# Formulas

Mission Two has this formula:
```M2 = 1 + [N_(fuel weight / time) / Max_(fuel weight / time] , where Max_(fuel weight / time) is the highest (fuel weight / time) score of all teams. ```

Mission Three:
```M3 = 2 + [N_(# laps flown + (bonus box score / X-1 test vehicle weight)) / Max_(# laps flown + (bonus box score / X1 test vehicle weight)] , where Max_(# laps flown + (bonus box score / X-1 test vehicle weight) is the highest (# laps flown + (bonus box score / X-1 test vehicle weight) score of all teams.```


# Max Values
Mission 1 is the easiest, we either get a point or we don't. We're assuming that if we cannot complete any mission, all subsequent missions are also a failure.

For M2 and M3, each maximum value can be determined(within reason) letting us graph our data in multiple sets assuming the worst(as in other teams having the best score possible) and best (we have the highest score, which equates to a score of 2 for m2 and 3 for m3)


_**For M2:**_
The denominator "max" is just the highest value of (fuel/time) by any competition team. The maximum weight of an aircraft is 55 lbs. This means the theoretical maximum would be closer to 45-50 lbs for fuel as the aircraft will take around 5-10 lbs (minimum)
The longest time in the air is about 5 minutes to complete 3 laps, but the shortest time is what we are all aiming for. We'll call it a minute thirty as a theoretical fastest model. We can work this back later as heavier aircraft may go slower.

This means (with a very generous set of scores) that a max value can start around 1.5. This means that the "max" value for M2 is 1.5, and our team's (fuel/time) will be divided by 1.5 to get a value between 1-2 points for M2. Keep in mind that for the best team with this score, this only nets them the max 1 point (team_fuelweight/max_fuelweight). The "max" value being higher just makes everyone elses score lower.

_**For M3:**_
This one is more complicated, but I'll skim the explanation and give my estimates as it is the same general idea as M2.
 - 8 laps max 
 - best boxscore of 2.5
 - best weight of 25g, 0.055 lbs

This gives us a "max" score of (8+2.5/0.055) or 53.4545455. Again, this is not the actual score but the denominator. Max points on the flight portion is 3 (2 completion, 1 bonus points)

# "**Reasonable**" Values
Our worst case scenario was those "max" values. These """reasonable""" values are just shy of the absurdity of the maxes but still a next-to-impossible score to get. 

To put it into context, a 55lb airplane with only a 6ft wingspan x 2ft chord nets a 4.58lb/sqft wing loading, where a 2.25lb/sqft wing loading is considered a heavy loading. Not to mention a max of 100a thrust. That is a very difficult aircraft to make and compete, much less doing that with a lap time of a minute thirty. Point being, the maxes are as close to impossible (if not straight up impossible entirely).

To get a better idea of our chances, these """reasonable""" values are trying to come up with a much more likely scenario for a potential best aircraft.

I'll skip my explanations and give my estimations:
 - M2 = 0.25
 - M3 = 26