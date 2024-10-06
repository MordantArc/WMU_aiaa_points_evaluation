# WMU AIAA Points Evaluation
Evaluates the possible points we can score in the 24-25 competition. Thats it

# Formulas

mission two has this formula:
```M2 = 1 + [N_(fuel weight / time) / Max_(fuel weight / time] , where Max_(fuel weight / time) is the highest (fuel weight / time) score of all teams. ```

mission three:
```M3 = 2 + [N_(# laps flown + (bonus box score / X-1 test vehicle weight)) / Max_(# laps flown + (bonus box score / X1 test vehicle weight)] , where Max_(# laps flown + (bonus box score / X-1 test vehicle weight) is the highest (# laps flown + (bonus box score / X-1 test vehicle weight) score of all teams.```


# Max Values
Mission 1 is the easiest, we either get a point or we dont. We're assuming that if we cannot complete a mission, all subsequent missions are also a failure.

For 2 and 3, each maximum value can be determined(within reason) letting us graph our data in multiple sets assuming the worst(as in other teams having the best score possible) and best (we have the highest score, which equates to a score of 2 for m2 and 3 for m3)


_**For M2:**_
The denominator is just the highest value of (fuel/time). The maximum weight of an aircraft is 55 lbs. This means the theoretical maximum would be closer to 45-50 lbs for fuel as the aircraft will take around 5-10 lbs (minimum)
The longest time is about 5 minutes, but ideally we have the shortest time to complete 3 laps. We'll call it a minute thirty as a theoretical fastest model. We can work this back later as heavier aircraft may go slower.

This means (with a very generous set of scores) that a max value can start around 1.5. Keep in mind that for the best team with this score, this only nets them the max 1 point (team_fuelweight/max_fuelweight). It just makes everyone elses score lower

_**For M3:**_
This one is more complicated, but I'll skim the explanation and give my estimates.
8 laps max 
best boxscore of 2.5
best weight of 25g, 0.055 lbs

this gives us a max score of (8+2.5/0.055) or 53.4545455. Again, this is not the actual score but the denominator. Max points on the flight portion is 3 (2 completion, 1 bonus points)

