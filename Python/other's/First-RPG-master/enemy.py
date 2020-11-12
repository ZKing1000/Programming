#!/usr/bin/env python

def enemy_Stats(type): #monster intial stats
    temp = 0
    if type == 'Frog': #if the monster is 'frog'
        temp = {
            'name': 'Frog',
            'hp': 120,'mp': 300,
            'maxhp': 120,'maxmp': 300,
            'def': 10,'res': 10,
            'str': 10,'dex': 10,
            'agi': 10,'spd': 10,
            'int': 10,'wsd': 10,
            'gsp': 10,
            'res': 10,'lck': 10,
            'pow': 15,'mpow': 15,
        }
    return temp