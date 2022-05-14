from pathlib import Path
import ipfsApi
import json
import os

JSON_FOLDER = 'json'
IMAGE_FOLDER = 'images'
TRACKER_FILE = 'ipfs_tracker.data'
LOG_FILE = 'ipfs_uploader.log'

START_OVER = False

log_file = open(LOG_FILE, 'a')

def writeToLog(line):
    log_file.write(line + '\n')

def countNumFiles(DIR):
    return len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])

def getLastUploadedFile():
    fle = Path(TRACKER_FILE)
    fle.touch(exist_ok=True)
    f = open(fle, 'r+')
    lines = f.readlines()
    if (len(lines) == 0):
        return 0

    return int(lines[-1])

base_url = 'https://ipfs.io/ipfs'

def updateJsonBlob(index, hash):
    blob_file = open(f"{JSON_FOLDER}/{index}", "r")
    json_object = json.load(blob_file)
    blob_file.close()

    json_object['image'] = f'{base_url}/{hash}'
    new_file = open(f"{JSON_FOLDER}/{index}", "w")
    json.dump(json_object, new_file, indent=4)
    new_file.close()

numJson = countNumFiles(JSON_FOLDER)

writeToLog('Connecting to ipfs')
api = ipfsApi.Client('127.0.0.1', 5001)

lastUploaded = getLastUploadedFile()
if (START_OVER):
    lastUploaded = 0

if (lastUploaded == numJson):
    exit(-1)

STOP_AT = 9300

if (numJson > STOP_AT):
    numJson = STOP_AT

#for i in range(lastUploaded+1, numJson+1):
for i in range(1, 3):
    print ('Uploaded NFT: ' + str(i))

    json_dir = '{}/{}'.format(JSON_FOLDER, i)
    image_dir = '{}/{}.png'.format(IMAGE_FOLDER, i)

    # Upload image
    res = api.add(image_dir)
    hash = res[0]['Hash']
    api.pin(hash)

    writeToLog('{} {}'.format(image_dir, hash))

    # Update json with image dir
    updateJsonBlob(i, hash)

    # Updload json
    res = api.add(json_dir)
    hash = res[0]['Hash']

    writeToLog('{} {}'.format(json_dir, hash))

    print ('Finished Uploading')

    with open(TRACKER_FILE, 'w') as f:
        f.write('{}\n'.format(i))


print ('Uploading json folder')
res = api.add(JSON_FOLDER, recursive=True)
hash = res['Hash']
print ('Finished')

writeToLog('{} {}'.format(JSON_FOLDER, hash))
writeToLog('Public folder: {}/{}'.format(base_url, hash))

log_file.close()