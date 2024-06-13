SECTION = 'RFID'
BTMIX_FILE = 'DB File'
DEVEL = 0
DEVEL = 1 # 1 for local development. Must be commented before deploy to photobooth
PLUGIN_ROOT = '/home/pi/pibooth/pibooth-rfid/'
if DEVEL:
    PLUGIN_ROOT = './' 
DATA_ROOT = PLUGIN_ROOT + 'data/' 
BTMIX_FILE_DEFAULT = DATA_ROOT + 'badges_db.json' #for photobooth
BADGES_IMG_FOLDER = 'Badge Folder'
BADGES_IMG_FOLDER_DEFAULT = DATA_ROOT + 'badges/' # for local development
BADGES_DEFAULT_IMG = 'Default image'
BADGES_DEFAULT_IMG_FILE = PLUGIN_ROOT + 'nobody.jpg'