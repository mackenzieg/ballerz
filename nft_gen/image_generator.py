from multiprocessing.pool import ThreadPool
try:
    from PIL import Image, ImageSequence
except ImportError:
    import Image
import shutil
from pathlib import Path
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
    return Image.open('Purple.png').convert('RGBA').resize((600, 338), Image.ANTIALIAS)

    #return Image.open(ATTRIBUTES_FOLDER + '/' + attribute + '/' + value + '.png').convert('RGBA')

def loadBackground(value):
    return Image.open('background.gif')
    #return Image.open('{}/Backgrounds/{}.gif'.format(ATTRIBUTES_FOLDER, value))

def countNumFiles(DIR):
    return len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])

def generateNFT(index):
    print ('Generating NFT: ' + str(index))

    f = open('{}/{}'.format(JSON_FOLDER, index), 'r')
    json_data = json.load(f)

    attributes = json_data['attributes']

    builtImage = None

    for trait in traitOrder:
        if ('Background' == trait):
            continue

        # Returns the value of the trait
        value = getValueFromAttributes(attributes, trait)

        if (value == 'None'):
            continue

        overlay = getImage(trait, value)

        if (builtImage is None):
            builtImage = overlay
        else:
            # Combine images together
            #builtImage = Image.alpha_composite(builtImage, overlay) 

            builtImage.paste(overlay, mask=overlay)

    background = getValueFromAttributes(attributes, 'Background')
    background = loadBackground(background)
        
    frames = []
    for frame in ImageSequence.Iterator(background):
        frame = frame.copy().convert('RGBA')
        frame.paste(builtImage, mask=builtImage)
        frames.append(frame)

    OUTPUT_FILE = '{}/{}.gif'.format(IMAGE_FOLDER, index)
    print ('Writing gif: ' + OUTPUT_FILE)

    frames[0].save(OUTPUT_FILE, save_all=True, append_images=frames[1:])

if __name__ == "__main__":
    jsonDir = Path(IMAGE_FOLDER)
    if jsonDir.is_dir():
        shutil.rmtree(IMAGE_FOLDER)

    os.makedirs(IMAGE_FOLDER)

    numFiles = countNumFiles(JSON_FOLDER)
    executor = ThreadPool(8)

    SETTINGS_FILE = 'settings.json'

    setting_file = Path(SETTINGS_FILE)
    if not setting_file.is_file():
        print ('Settings file missing... exiting')
        exit(-1)
    
    # Load settings
    json_file = open(SETTINGS_FILE, 'r')
    settings = json.load(json_file)
    json_file.close()

    if not 'trait_order' in settings:
        print ('Settings missing trait_order')
        exit(-1)

    traitOrder = []

    traitOrder = settings['trait_order']

    executor.map(generateNFT, range(1, numFiles+1))
    res.get(9300 * 100) # Without the timeout this blocking call ignores all signals.

    exit(-1)

    try:
        executor.map(generateNFT, range(1, numFiles+1))
        res.get(60) # Without the timeout this blocking call ignores all signals.
    except KeyboardInterrupt:
        executor.terminate()
    else:
        print("Normal termination")
        executor.close()
