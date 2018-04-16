#import pygame

#pygame.init()
#pygame.mixer.init()
#sounda= pygame.mixer.Sound("Alarm01.wav")

#sounda.play()

import time, sys
from pygame import mixer

# pygame.init()
mixer.init()

sound = mixer.Sound("wrongpos.wav")
sound.play()

time.sleep(5)
