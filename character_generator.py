import random
import numpy as np
import math

#Race_Choices = ['Human', 'Half-Elf', 'Elf', 'Dwarf', 'Half-Orc', 'Halfing', 'Tiefling', 'Dragonborn', 'Gnome']
#Class_Choices = ['Barbarian', 'Bard', 'Cleric', 'Druid', 'Fighter', 'Monk', 'Paladin', 'Ranger', 'Rogue', 'Sorcerer', 'Warlock', 'Wizard']

Race_Choices = ['Human', 'Half-Elf', 'Elf', 'Dwarf']
Class_Choices = ['Barbarian', 'Bard', 'Cleric', 'Druid', 'Fighter', 'Monk','Paladin']

subraces={
    'Elf':['High Elf', 'Wood Elf', 'Drow'],
    'Dwarf':['Hill Dwarf', 'Mountain Dwarf'],
}

subclasses={
    'Barbarian':['Berserker','Totem Warrior'],
    'Bard':['Lore', 'Valor'],
    'Cleric':['Knowledge', 'Life', 'Light', 'Nature', 'Tempest', 'Trickery', 'War'],
    'Druid':['Land', 'Moon'],
    'Fighter':['Champion', 'Battle Master', 'Eldritch Knight'],
    'Monk':['Open Hands', 'Shadow', 'Four Elements'],
    'Paladin':['Devotion', 'Ancients', 'Vengence'],
    'Ranger':['Hunter','Beast Master']
    
}



Selected_Race = random.choice(Race_Choices)
Selected_Class = random.choice(Class_Choices)
Selected_Subclass = random.choice(subclasses[Selected_Class])
if Selected_Race in subraces:
    Selected_SubRace = random.choice(subraces[Selected_Race])
else:
    Selected_SubRace = 'Normal'



character_level=4

standard_array=[15, 14, 13, 12, 10, 8]

hit_dice={
    'Barbarian':12,
    'Bard':8,
    'Cleric':8,
    'Druid':8,
    'Fighter':10
}

stat_priority={
    'Barbarian':{
        'strength': 1,
        'dexterity':2,
        'constitution':0,
        'intelligence':5,
        'wisdom':3,
        'charisma':4,
    },
    'Bard':{
        'strength': 3,
        'dexterity':1,
        'constitution':2,
        'intelligence':5,
        'wisdom':4,
        'charisma':0,
    },
    'Cleric':{
        'strength': 3,
        'dexterity':5,
        'constitution':2,
        'intelligence':4,
        'wisdom':0,
        'charisma':1,
    },
    'Druid':{
        'strength': 4,
        'dexterity':2,
        'constitution':1,
        'intelligence':3,
        'wisdom':0,
        'charisma':5,
    },
    'Fighter':{
        'strength': 0,
        'dexterity':2,
        'constitution':1,
        'intelligence':5,
        'wisdom':3,
        'charisma':4,
    },
}

stats={
        'strength': 0,
        'dexterity':0,
        'constitution':0,
        'intelligence':0,
        'wisdom':0,
        'charisma':0,
}





race_stats={
    'Human':{
        'strength': 1,
        'dexterity':1,
        'wisdom':1,
        'intelligence':1,
        'constitution':1,
        'charisma':1,
    },
    'Half-Elf':{
        'strength': 0,
        'dexterity':0,
        'wisdom':0,
        'intelligence':0,
        'constitution':0,
        'charisma':2,
    },
    'Elf':{
        'strength': 0,
        'dexterity':2,
        'wisdom':0,
        'intelligence':0,
        'constitution':0,
        'charisma':0,
    },
    'Dwarf':{
        'strength': 0,
        'dexterity':0,
        'wisdom':0,
        'intelligence':0,
        'constitution':2,
        'charisma':0,
    },

}


subrace_stats={
    'Normal':{
        'strength': 0,
        'dexterity':0,
        'wisdom':0,
        'intelligence':0,
        'constitution':0,
        'charisma':0,
    },
    'High Elf':{
        'strength': 0,
        'dexterity':0,
        'wisdom':0,
        'intelligence':1,
        'constitution':0,
        'charisma':0,
    },
    'Wood Elf':{
        'strength': 0,
        'dexterity':0,
        'wisdom':1,
        'intelligence':0,
        'constitution':0,
        'charisma':0,
    },
    'Drow':{
        'strength': 0,
        'dexterity':0,
        'wisdom':0,
        'intelligence':0,
        'constitution':0,
        'charisma':1,
    },
    'Hill Dwarf':{
        'strength': 0,
        'dexterity':0,
        'wisdom':1,
        'intelligence':0,
        'constitution':0,
        'charisma':0,
    },
    'Mountain Dwarf':{
        'strength': 2,
        'dexterity':0,
        'wisdom':0,
        'intelligence':0,
        'constitution':0,
        'charisma':0,
    },
}




def get_stats(character_race, character_class, character_subrace, stats=stats, priority=True, points='array'): 
    if points=='roll':
        array=[]
        for i in range(6):
            roll=0
            for j in range(3):
                roll+=random.randint(2,6)
            array.append(roll)
        array.sort(reverse=True)
    elif points=='array':
        array=[15, 14, 13, 12, 10, 8]
    
    if not priority:
        random.shuffle(array)

    for key in stats:
        stats[key]+=array[stat_priority[character_class][key]]
        stats[key]+=race_stats[character_race][key]
        stats[key]+=subrace_stats[character_subrace][key]
    return stats

def get_hit_points(level, character_class, average=False):
    hit_points=hit_dice[character_class]
    if average:
        for i in range(level):
            hit_points+=hit_dice[character_class]/2
        hit_points=math.floor(hit_points)
    else:
        for i in range(level):
            hit_points+=random.randint(1, hit_dice[character_class])
    return hit_points


print(get_stats(Selected_Race, Selected_Class, Selected_SubRace, priority=False, points='roll'), Selected_Race, Selected_SubRace, Selected_Class, Selected_Subclass)
print(get_hit_points(character_level, Selected_Class))
