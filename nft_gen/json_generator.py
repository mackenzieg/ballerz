import pandas as pd
import random
import numpy as np
import json
import csv
import os
import sys
import math
import shutil
from pathlib import Path

random.seed(10)

json_base_blob = {'name': 'Degen Waifus', 'description': 'asd', 'external_url': 'test_url', 'image': '', 'attributes': []}
JSON_FOLDER = 'json'
TRACKER_FILE = 'json_tracker.data'

def getLastUploadedFile():
    fle = Path(TRACKER_FILE)
    fle.touch(exist_ok=True)
    f = open(fle, 'r+')
    lines = f.readlines()
    if (len(lines) == 0):
        return 0

    return int(lines[-1])

def writeTeamJsonBlobs(json_blobs):
    lastTouchedJson = getLastUploadedFile()

    if (lastTouchedJson == len(json_blobs)):
        print ('All JSON already written... exiting')
        exit(-1)

    if (lastTouchedJson == 0):
        lastTouchedJson = 1

    for index in range(lastTouchedJson, len(json_blobs) + 1):
        with open(JSON_FOLDER  + '/' + str(index), 'w') as json_file:
            json.dump(json_blobs[index-1], json_file, indent=4)

        # Write last touched file        
        with open(TRACKER_FILE, 'w') as f:
            f.write('{}\n'.format(index))

def randomPickTraits(trait, teamQty, traitValues, traitQty):
    if (not teamQty == sum(traitQty)):
        sys.exit(trait + ' qty does not match team quantity. Difference: ' + str(teamQty - sum(traitQty)))
    
    pickedTraits = [None] * teamQty

    remainingIdx = range(1, teamQty+1)
    pickedIndex = []

    for i in range(len(traitQty)):
        validList = list(set(remainingIdx) - set(pickedIndex))
        picked = random.sample(validList, traitQty[i])

        pickedIndex.extend(picked)

        for idx in picked:
            pickedTraits[idx-1] = traitValues[i]

    return pickedTraits

def parseTraits(traits, fixedSkippedTeams, skippedTeams):
    json_blobs = []
    skipped_teams_blobs = []

    traitNames = list(traits.keys())
    traitNames.remove('Team Jersey')

    for team in traits['Team Jersey'].keys():
        print ('Starting processing team: ' + team)
        teamQty = traits['Team Jersey'][team]
        if (teamQty == 'N/A'):
            continue

        teamQty = int(teamQty)

        attributes = [[None for x in range(len(traitNames))] for y in range(teamQty)]

        traitCounter = 0

        for trait in traitNames:
            traitValues = list(traits[trait].keys())
            traitQty = list(map(int, traits[trait].values()))
            
            pickedTraits = randomPickTraits(trait, teamQty, traitValues, traitQty)

            index = 0
            for pickedTrait in pickedTraits:
                attribute = {'trait_type': trait, 'value': pickedTrait}

                attributes[index][traitCounter] = attribute

                index = index + 1

            traitCounter = traitCounter + 1

        attribute = {'trait_type': 'Team Jersey', 'value': team}
        for i in range(len(attributes)):
            attributes[i].insert(0, attribute)
            new_blob = json_base_blob
            new_blob['attributes'] = attributes[i]

            if (fixSkippedTeams and team in skippedTeams):
                skipped_teams_blobs.append(new_blob.copy())
            else:
                json_blobs.append(new_blob.copy())
        
        print ('Finished processing team: ' + team)

    random.shuffle(json_blobs)
    random.shuffle(skipped_teams_blobs)

    if (len(skipped_teams_blobs) > 0):
        json_blobs = json_blobs + skipped_teams_blobs

    print ('Starting JSON blob writing')
    writeTeamJsonBlobs(json_blobs)

if __name__ == "__main__":
    # Dictionary of all traits
    traits = {}
    nextLineTrait = False
    nextLinesData = 0
    trait = None

    tempNames = []
    tempQty = []

    print ('Starting CSV parsing')
    with open('Traits.csv', 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for i, line in enumerate(reader):
            if (nextLinesData):
                nextLinesData = nextLinesData + 1

                # Need to skip headers
                if (nextLinesData >= 4):
                    # End of table skip to next trait
                    if ('' == line[0]):
                        nextLinesData = 0

                        # Exiting table store found names and qty

                        traitData = dict(zip(tempNames, tempQty))

                        #traits[trait] = {'names': tempNames, 'qty': tempQty}
                        traits[trait] = traitData
                        tempNames.clear()
                        tempQty.clear()
                        continue

                    # In data for table
                    tempNames.append(line[1])
                    tempQty.append(line[3])

            if (nextLineTrait):
                nextLineTrait = False
                nextLinesData = 1

                # Parse out trait
                trait = line[1]

            if (line[1] == 'Trait'):
                nextLineTrait = True
    
    print ('Finished extracting CSV traits')

    print ('Writing settings file')

    allTraits = list(traits.keys())

    SETTINGS_FILE = 'settings.json'

    setting_file = Path(SETTINGS_FILE)
    if setting_file.is_file():
        print ('Settings file exists... exiting')
    else:
        # Start settings file defaults
        allTraits = list(traits.keys())
        settingsBlob = {'name': 'Ballerz', 'description': 'Cool project', 'external_url': 'Test'}
        settingsBlob['traits'] = allTraits
        settingsBlob['skipped_teams'] = ['United Arab Emirates', 'New Zealand', 'Scotland', 'Australia', 'Wales', 'Peru']
        settingsBlob['fix_skipped_teams'] = True

        with open(SETTINGS_FILE, 'w') as json_file:
            json.dump(settingsBlob, json_file, indent=4)

    # Load settings
    json_file = open(SETTINGS_FILE, 'r')
    settings = json.load(json_file)
    json_file.close()

    json_base_blob['name'] = settings['name']
    json_base_blob['description'] = settings['description']
    json_base_blob['external_url'] = settings['external_url']

    print ('Starting JSON blob generation')

    jsonDir = Path(JSON_FOLDER)
    if jsonDir.is_dir():
        shutil.rmtree(JSON_FOLDER)

    os.makedirs(JSON_FOLDER)

    fixSkippedTeams = settings['fix_skipped_teams']
    skippedTeams = settings['skipped_teams']

    parseTraits(traits, fixSkippedTeams, skippedTeams)
    print ('Finished JSON blob generation')

    
