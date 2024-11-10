from drawbadge import DrawBadge
from animation import Animation
from pibooth.utils import LOGGER
import json
import pygame
import time
import config
if config.DEVEL:
    from ntag.ntag_dummy import NtagReader
else:
    from ntag.ntag import NtagReader

class pbBadges:
    LIMIT_BADGES = 5
    attIds=[] # Attendee IDs
    debouncer = None
    def __init__(self,btMixFile : str, badgesImgFolder : str, badgesDefImg : str):
        self.btMixFile = btMixFile
        self.badgesImgFolder = badgesImgFolder
        self.attIds = []
        self.btdb = None
        self.badgesDefImg = badgesDefImg
        try:
            with open(btMixFile, "r") as f:
                btwrapper = json.load(f)
                self.btdb = btwrapper["items"]
            LOGGER.debug("Badges init")
        except FileNotFoundError as e:
            LOGGER.error(f"File {btMixFile} doesn't exist!")

    def startAdding(self, win):
        self.animation = Animation(win)
        self.drawbadge = DrawBadge( self.btdb, self.badgesImgFolder, self.badgesDefImg, win)
        self.reader = NtagReader()
        self.attIds = []
        self.deboucer = None
        rfidSymbolRect = pygame.Rect(20,20,175,150)
        win_rect = win.get_rect()
        rfidSymbolRect.topright = win_rect.topright
        self.animation.start(config.BADGES_RFID_GIF, rfidSymbolRect)
        LOGGER.debug("Badges Start")

    def led(self, stateOK : bool ):
        if hasattr(self,"app") and hasattr(self.app, "pibooth_ledstrip"):
                        self.app.pibooth_ledstrip.badge(stateOK)

    def add(self, id : int):
        if id:
            if id not in self.attIds:
                if len(self.attIds) <= self.LIMIT_BADGES:
                    self.attIds.append(id)
                    self.drawbadge.add(id)
                    self.led(True)

    
    def addBadge(self,badge):
        if badge and self.btdb:
            badge_str = bytes(badge).hex().casefold()
            LOGGER.info(f"read badge - debounced: {badge_str}")
            found = next((bt for bt in self.btdb if bt["uid"].casefold() == badge_str), None )
            if found:
                if "id" in found:
                    id = found["id"]
                    self.add(id)
                    LOGGER.debug(f"added badge: {badge_str}")
                    
                    return id
                else:
                    LOGGER.error(f"(ignored) Nonexisting badge ID: {badge_str}")
                    self.led(False)
            else:
                LOGGER.error(f"(ignored) Nonexisting badge: {badge_str}")
                self.led(False)

    def do(self, showLogo = True):
        if showLogo:
            self.animation.animate(500)
            
        badge = self.reader.read_id_no_block()
        if badge:
            # LOGGER.debug(f"read badge: {bytes(badge).hex()}")
            self.errorCount = 0
            if ( not badge == self.deboucer ):
                self.deboucer = badge
                return self.addBadge( badge )
        else: # badge = None
            if self.debouncer:
                errorCount += 1
                if errorCount > 2: #every second reading goes wrong so we're waiting for at least two invalid reading here.
                    self.debouncer = None

    def redraw(self):
        self.drawbadge.redraw()
    def exitAdding(self):
        self.reader.Close()
        del self.drawbadge
        del self.reader
        del self.animation
    
    def getIDs(self):
        meta = {}
        for id in self.attIds:
            meta.update({f"id{id}":id})
        return meta
    
    def getJSON(self, file):
        items=[]
        for attID in self.attIds:
            items.append({"attid" : attID})
        wrapper={"name" : "Photobooth read badges",
                             "timestamp" : time.time(),
                             "items" : items }
        json.dump(wrapper,file, indent=1)

    def writeJson(self , path):
        with open(path, "w") as f:
            LOGGER.debug(f"writing {path}")
            self.getJSON(f)

    