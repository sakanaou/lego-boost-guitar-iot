import re
import paho.mqtt.client as mqtt
import pygame.mixer, pygame.sndarray
import samplerate

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("guitar/+")

def on_message(client, userdata, msg):
    global snd_blue, snd_red, snd_cyan, snd_yellow
    match = re.match("guitar/([^/]+)", msg.topic)
    event_type = match.group(1)
    
    if event_type == "color":
        color = msg.payload.decode()
        if color == "BLUE":
            snd_blue.play()
        elif color == "RED":
            snd_red.play()
        elif color == "CYAN":
            snd_cyan.play()
        elif color == "YELLOW":
            snd_yellow.play()
    elif event_type == "motor_a":
        angle = int(msg.payload)
        snd_blue = pitch(orig_snd_blue, angle)
        snd_red = pitch(orig_snd_red, angle)
        snd_cyan = pitch(orig_snd_cyan, angle)
        snd_yellow = pitch(orig_snd_yellow, angle)

def pitch(snd, angle):
    snd_array = pygame.sndarray.array(snd)
    snd_resample = samplerate.resample(snd_array, 0.85 + (angle * 1.0 / 360.0) * 0.3, "sinc_fastest").astype(snd_array.dtype)
    return pygame.sndarray.make_sound(snd_resample)

pygame.mixer.init(44100,-16,8,4096)

orig_snd_blue = pygame.mixer.Sound("BLUE.wav")
orig_snd_red = pygame.mixer.Sound("RED.wav")
orig_snd_cyan = pygame.mixer.Sound("CYAN.wav")
orig_snd_yellow = pygame.mixer.Sound("YELLOW.wav")
snd_blue = orig_snd_blue
snd_red = orig_snd_red
snd_cyan = orig_snd_cyan
snd_yellow = orig_snd_yellow

print("Connecting to Mosquitto...")
mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.connect("localhost", 1883)

mqttc.loop_forever()
