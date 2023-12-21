import re
import numpy as np
import urllib.request
import requests
from bs4 import BeautifulSoup



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



class lookup_stats:
    def __init__(self, url):
        self.Dict = {
            'Name' : '',
            'CR' : '',
            'XP' : '',
            'Race' : '',
            'Class' : '',
            'MonsterSource':'',
            'Alignment': '',
            'Size': '',
            'Type': '',
            'SubType': '',
            'Init': '',
            'Senses': '',
            'Aura': '',
            'AC': '',
            'AC_Mods': '',
            'HP': '',
            'HD': '',
            'HP_Mods': '',
            'Saves': '',
            'Fort': '',
            'Ref': '',
            'Will': '',
            'Save_Mods': '',
            'Defensive Abilities': '',
            'DR': '',
            'Immune': '',
            'Resist': '',
            'SR': '',
            'Weaknesses': '',
            'Speed': '',
            'Speed_Mod': '',
            'Melee': '',
            'Ranged': '',
            'Space': '',
            'Reach': '',
            'Special Attacks': '',
            'Spell Like Abilities': '',
            'Spells Known': '',
            'Spells Prepared': '',
            'Spell Domains': '',
            'Abilitiy Scores': '',
            'AbilitiyScore_Mods': '',
            'Base Atk': '',
            'CMB': '',
            'CMD': '',
            'Feats': '',
            'Skills': '',
            'Racial Modifiers': '',
            'Languages': '',
            'SQ': '',
            'Environment': '',
            'Organization': '',
            'Treasure': '',
                    }
        soup = BeautifulSoup(requests.Session().get(url).content,"html5lib")
        self.text = soup.get_text()
        self.Dict['Name'] = re.findall('\n\s*(.*) CR \d*\/?\d*\s*\n', self.text)[0]
        self.relevent_text = re.findall(self.Dict['Name'] + ' CR \d*[\S\s]*', self.text)[0]
        self.relevent_text = self.relevent_text.replace(u"\U00002013", "-")
        self.cat_split = re.split('DEFENSE|OFFENSE|TACTICS|STATISTICS|SPECIAL ABILITIES|ECOLOGY',self.relevent_text)


        self.list_of_classes = ['Barbarian', 'Bard', 'Cleric', 'Druid', 'Fighter', 'Monk', 'Paladin',
                   'Ranger', 'Rogue', 'Sorcerer', 'Wizard', 'Alchemist', 'Cavalier', 'Gunslinger',
                   'Inquisitor', 'Magus', 'Omdura', 'Oracle', 'Shifter', 'Summoner', 'Witch', 'Vampire Hunter', 'Vigilante',
                    'Arcanist', 'Bloodrager', 'Brawler', 'Hunter', 'Investigator', 'Shaman', 'Skald', 'Slayer',
                    'Swashbuckler', 'Warpriest', 'Kineticist', 'Medium', 'Mesmerist', 'Occultist', 'Psychic', 'Spiritualist',
                    'Antipaladin', 'Ninja', 'Samurai', 'Adept', 'Aristocrat', 'Commoner', 'Expert', 'Warrior']

        #for box in range(len(self.cat_split)):
        #    print(box)
        #    print(self.cat_split[box])

    def get_top_layer(self):

        self.Dict['CR'], self.Dict['XP'] = re.findall(self.Dict['Name']+'\s*CR\s*(.*)\s*XP (\d*,?\d*)',self.cat_split[0])[0]
        self.Dict['Alignment'], self.Dict['Size'] =  re.findall('([A-Z][A-Z]?) ([a-zA-Z][a-z]+)', self.cat_split[0])[0]
        self.Dict['Type'] = re.findall(self.Dict['Size'] + '\s*([\S\s]*?)(?:\(|Init)', self.cat_split[0])[0]
        self.Dict['SubType'] = re.findall(self.Dict['Type'] + '\s*([\S\s]*?)(?:Init)', self.cat_split[0])[0]
        if 'Aura' in self.cat_split[0]:
            self.Dict['Init'], self.Dict['Senses'], self.Dict['Aura'] = re.findall('Init\s*(.?\d*)\;\s*Senses\s*(.*)\s*Aura\s*(.*)', self.cat_split[0])[0]
        else:
            self.Dict['Init'], self.Dict['Senses'] = re.findall('Init\s*(.?\d*)\;\s*Senses\s*(.*)', self.cat_split[0])[0]
        race_class = re.findall(self.Dict['XP'] + '\s*((?:(?!\s*'+self.Dict['Alignment']+').)*)', self.cat_split[0])[0]
        if race_class.upper().isupper():
            if race_class[-1].isnumeric():
                if len(race_class.split(' ')) ==3:
                    race = race_class.split(' ')[0]
                    cla = race_class.split(' ')[0] + ' ' + race_class.split(' ')[0]
                else:
                    for class_name in self.list_of_classes:
                        if class_name.casefold() in race_class.casefold():
                            race, cla = re.findall('(.*)(' + class_name.casefold() + '.*)',race_class.casefold())[0]
                            break
            else:
                race = race_class
                cla = ''
        else:
            race = ''
            cla = ''
        self.Dict['Race'] = race
        self.Dict['Class'] = cla

    def get_defense(self):

        self.Dict['AC'], self.Dict['AC_Mods'] = re.findall('AC (\d*,\s*touch \d*, flat-footed \d*) (\([\S|\s]*[a-z]\))\s*(?:hp|Fort)', self.cat_split[1])[0]
        self.Dict['HP'], self.Dict['HD'] = re.findall(r'\s*hp\s*(\d*)\s*(\([\S|\s]*\))', self.cat_split[1])[0]#self.defense_stats[2]

        self.Dict['Saves'] = re.findall('\s*(Fort [\S\s]*?)(?:\Z|Def|Imm|Resis|Weak)',self.cat_split[1])[0]
        self.Dict['Fort'] =  re.findall('Fort\s*(.*)',self.Dict['Saves'])[0]
        self.Dict['Ref'] = re.findall('Ref\s*(.*)',self.Dict['Saves'])[0]
        self.Dict['Will'] = re.findall('Will\s*(.*)',self.Dict['Saves'])[0]


        if 'Defensive Abilities' in self.cat_split[1]:
            self.Dict['Defensive Abilities'] = re.findall(r'Defensive Abilities ([\S\s]*?)(?:\Z|;)', self.cat_split[1])[0]

        if 'Immune' in self.cat_split[1]:
            self.Dict['Immune'] = re.findall(r'Immune ([\S\s]*?)(?:\Z|;)', self.cat_split[1])[0]

        if 'Resist' in self.cat_split[1]:
            self.Dict['Resist'] = re.findall(r'Resist ([\S\s]*?)(?:\Z|[A-Z])', self.cat_split[1])[0]

        if 'Weaknesses' in self.cat_split[1]:
            self.Dict['Weaknesses'] = re.findall(r'Weaknesses ([\S\s]*?)(?:\Z|[A-Z])', self.cat_split[1])[0]

        if 'DR ' in self.cat_split[1]:
            self.Dict['DR'] = re.findall(r'DR ([\S\s]*?)(?:\Z|;)', self.cat_split[1])[0]

        if 'SR' in self.cat_split[1]:
            self.Dict['SR'] = re.findall(r'SR (\d*)', self.cat_split[1])[0]

    def get_offense(self):
        self.Dict['Speed'] = re.findall(r'Speed ((?:(?!Melee|Ranged|Space|Reach|Special Attack|Spell)[\S\s])*)',self.cat_split[2])[0]
        if 'Melee' in self.cat_split[2]:
            self.Dict['Melee'] = re.findall(r'Melee ((?:(?!Ranged|Space|Reach|Special Attack|Spell)[\S\s])*)',self.cat_split[2])[0]
        if 'Ranged' in self.cat_split[2]:
            self.Dict['Ranged'] = re.findall(r'Ranged ((?:(?!Space|Reach|Special Attack|Spell)[\S\s])*)',self.cat_split[2])[0]

        if 'Space' in self.cat_split[2]:
            self.Dict['Space'] = re.findall(r'Space ((?:(?!Reach|Special Attack|Spell)[\S\s])*)',self.cat_split[2])[0]

        if 'Reach' in self.cat_split[2]:
            self.Dict['Reach'] = re.findall(r'Reach ((?:(?!Special Attacks|Spell)[\S\s])*)',self.cat_split[2])[0]

        if 'Special Attacks' in self.cat_split[2]:
            self.Dict['SpecialAttacks'] = re.findall(r'Special Attacks ((?:(?!Spell)[\S\s])*)',self.cat_split[2])[0]

        if 'Spell-Like' in self.cat_split[2]:
            if 'Spells Known' in self.cat_split[2]:
                self.Dict['Spell Like Abilities'] = re.findall(r'Spell\WLike Abilities ((?:(?!([A-Z]\w*)?\s*Spells)[\S\s])*)',self.cat_split[2])[0]
                if len(self.Dict['Spell Like Abilities']) > 1:
                    self.Dict['Spell Like Abilities'] = self.Dict['Spell Like Abilities'][0]
            else:
                self.Dict['Spell Like Abilities'] = re.findall(r'Spell\WLike Abilities (.*)',self.cat_split[2])[0]

        if 'Spells Known' in self.cat_split[2]:
            self.Dict['Spells Known'] = re.findall(r'Spells Known ([\S\s]*)',self.cat_split[2])[0]

    def get_statistics(self):


        #Sometimes there is a TACTICS section before the STATISTICS section.
        #This effects the index of cat_split that should be used
        for i in range(len(self.cat_split)):
            find_section = re.findall(r'(Str[\S|\s]*Cha\s\d*)',self.cat_split[i])
            if len(find_section) > 0:
                sec=i
                break
        self.Dict['Abilitiy Scores'] = re.findall(r'(Str[\S|\s]*Cha\s\d*)',self.cat_split[sec])[0]
        self.Dict['Base Atk'] = re.findall(r'Base\s*Atk\s(\W?\d*)', self.cat_split[sec])[0]
        self.Dict['CMB'] = re.findall(r'CMB([\S|\s]*)CMD\s*\d*\s*', self.cat_split[sec])[0]
        self.Dict['CMD'] = re.findall(r'CMD\s((?:(?!\s*[A-Z]).)*)', self.cat_split[sec])[0]
        if 'Feats' in self.cat_split[sec]:
            self.Dict['Feats'] = re.findall(r'Feats\s((?:(?!\s*Skills|Racial|Languages|SQ).)*)', self.cat_split[sec])[0]

        if 'Skills' in self.cat_split[sec]:
            self.Dict['Skills'] = re.findall(r'Skills\s((?:(?!\s*Racial|Languages|SQ).)*)', self.cat_split[sec])[0]
        if 'Racial Mod' in self.cat_split[sec]:
            self.Dict['Racial Modifiers'] = re.findall(r'Racial\sModifiers\s((?:(?!\s*Languages|SQ).)*)', self.cat_split[sec])[0]
        if 'Languages' in self.cat_split[sec]:
            self.Dict['Languages'] = re.findall(r'Languages\s((?:(?!\s*SQ).)*)', self.cat_split[sec])[0]
        if ' SQ ' in self.cat_split[sec]:
            self.Dict['SQ'] = re.findall(r'\sSQ\s(.*)', self.cat_split[sec])[0]



    def _clean_it_up(self):
        for key in self.Dict:
            if '\n' in self.Dict[key]:
                self.Dict[key] = self.Dict[key].replace('\n', ' ')
            if len(self.Dict[key]) > 0:
                if self.Dict[key][0] == ' ':
                    self.Dict[key] = self.Dict[key][1:]
                if self.Dict[key][-1] == ' ':
                    self.Dict[key] = self.Dict[key][:-1]


    def get_em_all(self):
        self.get_top_layer()
        self.get_defense()
        self.get_offense()
        self.get_statistics()
        self._clean_it_up()
        return self.Dict
