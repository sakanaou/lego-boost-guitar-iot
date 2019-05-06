import time
import random
import paho.mqtt.client as mqtt

mqttc = mqtt.Client()
mqttc.connect("localhost", 1883, 60)
mqttc.loop_start()

colors = ["RED", "CYAN", "BLUE", "YELLOW"]

events = ["voltage", "bump", "color", "motor_a", "motor_b"]

while True:
    event = random.choice(events)

    if event == "voltage":
        mqttc.publish("guitar/voltage", random.random())
    elif event == "color":
        mqttc.publish("guitar/color", random.choice(colors))
    elif event == "bump":
        mqttc.publish("guitar/bump", 1)
    elif event == "motor_a":
        mqttc.publish("guitar/motor_a", random.randint(0, 360))
    elif event == "motor_b":
        mqttc.publish("guitar/motor_b", random.randint(-1024, 1024))

    time.sleep(random.random() * 2)
