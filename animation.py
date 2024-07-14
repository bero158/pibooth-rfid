from pibooth.utils import LOGGER
import os
import pygame
from pibooth import pictures, fonts
import time
from PIL import Image, ImageSequence

# https://stackoverflow.com/questions/29571399/how-can-i-load-an-animated-gif-and-get-all-of-the-individual-frames-in-pygame?noredirect=1

class Animation:
    frameNr = 0
    position = None
    frames = None
    animLastChange = 0

    def __init__(self, win):
        self.win = win

    def pilImageToSurface(self,pilImage):
        mode, size, data = pilImage.mode, pilImage.size, pilImage.tobytes()
        return pygame.image.fromstring(data, size, mode).convert_alpha()

    def loadGIF(self,imgPath):
        pilImage = Image.open(imgPath)
        frames = []
        if pilImage.format == 'GIF' and pilImage.is_animated:
            for frame in ImageSequence.Iterator(pilImage):
                pygameImage = self.pilImageToSurface(frame.convert('RGBA'))
                frames.append(pygameImage)
        else:
            frames.append(self.pilImageToSurface(pilImage))
        return frames
    
    def start(self, imgPath : str, position : pygame.Rect):
        self.frameNr = 0
        self.position = position
        self.frames = self.loadGIF(imgPath)
    

    def draw(self, picture):
            if not self.win:
                return
            
            picture = pygame.transform.scale(picture,self.position.size)
            # self.drawFrame(self.position, win.surface)
            self.win.surface.blit(picture,self.position)

    def animate(self, delay = 0):
            if not self.frames:
                return
            
            if self.frameNr >= len(self.frames):
                 self.frameNr = 0

            self.draw(self.frames[self.frameNr])
            if delay:
                now = time.time()
                if (now - self.animLastChange)*1000 > delay:
                    self.frameNr += 1
                    self.animLastChange = time.time()
            else:
                self.frameNr += 1
            