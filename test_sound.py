import pygame.mixer, pygame.sndarray
import samplerate
import time

pygame.mixer.init(44100,-16,8,4096)

snd_blue = pygame.mixer.Sound("BLUE.wav")
snd_red = pygame.mixer.Sound("RED.wav")
snd_cyan = pygame.mixer.Sound("CYAN.wav")
snd_yellow = pygame.mixer.Sound("YELLOW.wav")

#snd_blue.play()
#snd_red.play()
#snd_cyan.play()
#snd_yellow.play()

snd_array = pygame.sndarray.array(snd_blue)
snd_resample = samplerate.resample(snd_array, 0.5 + (0.0 / 180.0), "sinc_fastest").astype(snd_array.dtype)
snd_out = pygame.sndarray.make_sound(snd_resample)

snd_out.play()

time.sleep(5)
