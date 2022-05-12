from multiprocessing.pool import ThreadPool
try:
    from PIL import Image
except ImportError:
    import Image
import json
import os

JSON_FOLDER = 'json'
IMAGE_FOLDER = 'images'

ATTRIBUTES_FOLDER = 'attributes'

def getValueFromAttributes(attributes, key):
    for dic in attributes:
        if (key == dic['trait_type']):
            return dic['value']

    return None

def getImage(attribute, value):
    return None
    return Image.open(ATTRIBUTES_FOLDER + '/' + background + '/' + value + '.png').convert('RGBA')

def countNumFiles(DIR):
    return len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])

def generateNFT(index):
    print ('Generating NFT: ' + str(index))

    f = open('{}/{}'.format(JSON_FOLDER, index), 'r')
    json_data = json.load(f)

    attributes = json_data['attributes']

    background = getValueFromAttributes(attributes, 'Background')

    backgroundImage = getImage('Background', background)

    for attribute in attributes:
        trait = attribute['trait_type']
        value = attribute['value']

        if (value is 'None'):
            continue

        overlay = getImage(trait, value)

        #backgroundImage = Image.alpha_composite(backgroundImage, overlay) 

if __name__ == "__main__":
    numFiles = countNumFiles(JSON_FOLDER)
    executor = ThreadPool(20)

    try:
        executor.map(generateNFT, range(1, numFiles+1))
        res.get(60) # Without the timeout this blocking call ignores all signals.
    except KeyboardInterrupt:
        executor.terminate()
    else:
        print("Normal termination")
        executor.close()
