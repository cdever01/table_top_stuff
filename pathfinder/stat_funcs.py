import re
import numpy as np




def get_hit_dice(data):
    hit_dice_list = list(filter(None, re.split(' |(\+|\-)',data['HD'][1:-1])))
    unfiltered = [re.findall(r'\d+d\d+',i) for i in hit_dice_list]
    hit_dice = [i[0].split('d') for i in unfiltered if len(i)>0]

    total_hit_dice = 0
    for dice in hit_dice:
        total_hit_dice += float(dice[0])
    return total_hit_dice, hit_dice

def get_stats(data):
    stats = [stat.split() for stat in data['Abilitiy Scores'].split(', ')]
    return stats

def get_saves(data):
    saves = [save.split(' ') for save in data['Saves'].split(', ')]
    return saves

def get_attacks(data,me_ra='Melee'):
    attack = data[me_ra]
    if attack == 0:
        attack = '0'
    if 'Special Attack' in attack:
        attack=attack.split(' Special Attack')[0]
    attack = re.split(' or ', attack)
    attack = [re.findall(r'([+-]?\d?) ?([a-zA-Z[ a-zA-Z]*]*) ((?:[+-]\d*\/?[+-]?\d*)*) (\(.*?\))' ,full_round) for full_round in attack]
    for fr in range(len(attack)):
        for at in range(len(attack[fr])):
            attack[fr][at] = [atta for atta in attack[fr][at] if atta !='']
    return attack



def print_it_out(Dict):
    BOLD = '\033[1m'
    END = '\033[0m'
    top_box = str(BOLD + Dict['Name'] + '\tCR '+ Dict['CR'] + '\n'+
              'XP\t' + Dict['XP'] + END + '\n' +
               Dict['Race'] +' '+ Dict['Class'] + '\n' +
               Dict['Alignment'] + '     ' + Dict['Size'] + '     ' +
               Dict['Type'] + ' ' + Dict['SubType'] + '\n')
    
    top_box += BOLD + 'Init ' + END + Dict['Init'] + '; '
    if Dict['Senses'] != '':
        top_box += BOLD + 'Senses ' + END + Dict['Senses']
    top_box += '\n'
    if Dict['Aura'] != '':
        top_box += BOLD +'Aura ' + END + Dict['Aura'] + '\n'
    Defense_box = str(BOLD + 'AC ' + END+ Dict['AC'] + ' ' + Dict['AC_Mods'] + '\n' + BOLD +'hp ' + END+ Dict['HP']
                          + ' (' + Dict['HD'] + ')\n' + Dict['Saves'] + '\n')
    Def_keys = ['Defensive Abilities', 'DR', 'Immune', 'Resist', 'Weaknesses']
    for key in Def_keys:
        if Dict[key] != '':
            Defense_box += BOLD + key +END + ' ' + Dict[key] + ' '
            if len(Defense_box.split('\n')[-1]) > 10:
                Defense_box += '\n'

    Offense_box = ''
    Offense_box += BOLD + 'Speed ' + END + Dict['Speed'] + '\n'
    Off_keys = ['Melee', 'Ranged', 'Space', 'Reach', 'Special Attacks',
                'Spell Like Abilities', 'Spells Known', 'Spells Prepared', 'Spell Domains']

    for key in Off_keys:
        if Dict[key] != '':
            Offense_box += BOLD + key + END + ' ' + Dict[key] + ' '
            if len(Offense_box.split('\n')[-1]) > 10:
                Offense_box += '\n'
        
    Statistics_box = ''
    Statistics_box += Dict['Abilitiy Scores'] + '\n'
        
    stat_keys = ['Base Atk', 'CMB', 'CMD', 'Feats', 'Skills', 'Languages', 'SQ']
    for key in stat_keys:
        if Dict[key] != '':
            Statistics_box += BOLD + key + END + ' ' + Dict[key] + ' '
            if len(Statistics_box.split('\n')[-1]) > 10:
                Statistics_box += '\n'
                    
    print(top_box)
    print('--------------------------------------------------------------')
    print('DEFENSE')
    print('--------------------------------------------------------------')
    print(Defense_box)
    print('--------------------------------------------------------------')
    print('OFFENSE')
    print('--------------------------------------------------------------')
    print(Offense_box)
    print('--------------------------------------------------------------')
    print('STATISTICS')
    print('--------------------------------------------------------------')
    print(Statistics_box)
