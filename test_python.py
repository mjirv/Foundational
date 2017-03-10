import glob
import json
from pprint import pprint

class Payload(object):
    def __init__(self, j):
        self.__dict__ = json.loads(j)

class Person(object):
    def __init__(self, name, openness, neuroticism, extraversion, conscientiousness, agreeableness):
        self.name = name

        self.openness = openness
        self.neuroticism = neuroticism
        self.extraversion = extraversion
        self.conscientiousness = conscientiousness
        self.agreeableness = agreeableness
        
        self.rewards = False
        self.social_attention = False
        self.communal_goals = False
        self.interpersonal_harmony = False
        self.achievement = False
        self.order = False
        self.efficiency = False
        self.threats = False
        self.uncertainty = False
        self.creativity = False
        self.innovation = False
        self.intellectual_stimulation = False
        
        if extraversion > .7:
            self.rewards = True
            self.social_attention = True
        if agreeableness > .7:
            self.communal_goals = True
            self.interpersonal_harmony = True
        if conscientiousness > .7:
            self.achievement = True
            self.order = True
            self.efficiency = True
        if neuroticism > .7:
            self.threats = True
            self.uncertainty = True
        if openness > .7:
            self.creativity = True
            self.innovation = True
            self.intellectual_stimulation = True
    
    def __str__(self):
        personality = {'openness': self.openness, 'neuroticism': self.neuroticism, 'extraversion': self.extraversion, 'conscientiousness': self.conscientiousness, 'agreeableness': self.agreeableness}
        receptive_to = {'rewards': self.rewards, 'social_attention': self.social_attention, 'communal_goals': self.communal_goals, 'interpersonal_harmony': self.interpersonal_harmony, 'achievement': self.achievement, 'order': self.order, 'efficiency': self.efficiency, 'threats': self.threats, 'uncertainty': self.uncertainty, 'creativity': self.creativity, 'innovation': self.innovation, 'intellectual_stimulation': self.intellectual_stimulation}
        return "{'" + self.name + "': \n'Personality': " + str(personality) +"\n" + "'Receptive to': " + str(receptive_to) + "}"

for filename in glob.iglob('@*.json'):
    with open(filename) as data_file:
        data = json.load(data_file)

        p = Payload(str(data).replace("'",'"').replace("Emotional range", "Neuroticism"))

        dictionary = {'openness' : 0.0, 'neuroticism': 0.0, 'extraversion': 0.0, 'conscientiousness': 0.0, 'agreeableness': 0.0}
        for i in p.personality:
            dictionary[i['name'].lower()] = i['percentile']
        
        test_person = Person(filename[:filename.find("_")], dictionary['openness'], dictionary['neuroticism'], dictionary['extraversion'], dictionary['conscientiousness'], dictionary['agreeableness'])
        print(test_person)
        print("")
        print("")
