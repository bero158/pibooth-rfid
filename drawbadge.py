# https://documentation.pibooth.org/en/stable/sources/plugins/examples.html#add-get-ready-text-before-captures-sequence
# from ast import Try
from pibooth.utils import LOGGER
import os
import pygame
from pibooth import pictures, fonts


class DrawBadge:
    MAX_POS = 6
    def __init__(self,btdb , badgesImgFolder : str, defImg : str, win):
        self.badgesImgFolder = badgesImgFolder
        self.ids = []
        self.win = win
        self.btdb = btdb
        self.defImg = defImg

        LOGGER.debug("DrawBadge init")

    def drawFrame(self, rect, surface):
        frame_rect = rect.inflate(4,4)
        color = pygame.Color(255,255,255)
        pygame.draw.rect(surface,color, frame_rect, 4) 
       
    def secImgLoad(self,imgPath):
        picture = None
        if not imgPath:
            return None
        try:
            picture = pygame.image.load(imgPath).convert()
        except:
            LOGGER.error(f"{imgPath} can't be read!")
            
        return picture

    def drawImg(self, imgPath : str, position : int, win):
        size = (80,80)
        if not win:
            return
        if not position in range(0,self.MAX_POS):
            return
        win_rect = win.get_rect()
        picture = self.secImgLoad( imgPath )
        if not picture:
            picture = self.secImgLoad( self.defImg )
        if not picture:
            return
        picture = pygame.transform.scale(picture,size)
        pic_rect = picture.get_rect(bottomright=win_rect.bottomright)
        y = ((pic_rect.height + 10 ) * position ) + 20
        pic_rect = pic_rect.move(-20, 0 - y)
        self.drawFrame(pic_rect, win.surface)
        win.surface.blit(picture,pic_rect)

    def drawImgId(self, badge : int, position : int ):
        if (badge>0 and position in range(0,self.MAX_POS)):
            imgPath = os.path.join(self.badgesImgFolder,str( badge ) + os.extsep + "jpg")
            self.drawImg(imgPath, position , self.win)
       

    def add(self, id):
        if id not in self.ids:
            self.ids.append(id)
            self.drawImgId(id, len(self.ids)-1 )
        
        # Force screen update and events process
        pygame.display.update()
        pygame.event.pump()