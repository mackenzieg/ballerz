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
    return Image.open(ATTRIBUTES_FOLDER + '/' + attribute + '/' + value + '.png').convert('RGBA')

def loadBackground(value):
    return Image.open('{}/Backgrounds/{}.gif'.format(ATTRIBUTES_FOLDER, value))

def countNumFiles(DIR):
    return len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])

def generateNFT(index, traitOrder):
    print ('Generating NFT: ' + str(index))

    f = open('{}/{}'.format(JSON_FOLDER, index), 'r')
    json_data = json.load(f)

    attributes = json_data['attributes']

    builtImage = None

    for trait in traitOrder:
        if ('Background' == trait):
            continue

        # Returns the value of the trait
        value = getValueFromAttributes(trait)

        if (value is 'None'):
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

    frames[0].save('output.gif', save_all=True, append_images=frames[1:])

if __name__ == "__main__":
    numFiles = countNumFiles(JSON_FOLDER)
    executor = ThreadPool(20)

    traitOrder = []

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

    traitOrder = settings['trait_order']

    try:
        executor.map(generateNFT, range(1, numFiles+1), traitOrder)
        res.get(60) # Without the timeout this blocking call ignores all signals.
    except KeyboardInterrupt:
        executor.terminate()
    else:
        print("Normal termination")
        executor.close()
