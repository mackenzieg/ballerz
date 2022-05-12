import pandas as pd
import random
import numpy as np
import json
import csv
import os
import sys
import math

random.seed(10)

json_base_blob = {'name': 'Degen Waifus', 'description': 'asd', 'external_url': 'test_url', 'image': '', 'attributes': []}
JSON_FOLDER = 'json'

def writeTeamJsonBlobs(json_blobs):
    for index in range(len(json_blobs)):
        with open(JSON_FOLDER  + '/' + str(index + 1), 'w') as json_file:
            json.dump(json_blobs[index], json_file, indent=4)

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

def parseTraits(traits):

    traitNames = list(traits.keys())
    traitNames.remove('Team Jersey')

    for team in traits['Team Jersey'].keys():
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
            json_blobs.append(new_blob.copy())

    random.shuffle(json_blobs)

    writeTeamJsonBlobs(json_blobs)

if __name__ == "__main__":
    # Dictionary of all traits
    traits = {}
    nextLineTrait = False
    nextLinesData = 0
    trait = None

    tempNames = []
    tempQty = []


    json_blobs = []

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
    
    parseTraits(traits)
