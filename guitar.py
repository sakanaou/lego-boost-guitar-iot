from pylgbst.movehub import MoveHub, TiltSensor, ColorDistanceSensor, EncodedMotor
from pylgbst.comms.cpygatt import BlueGigaConnection
import paho.mqtt.client as mqtt
#import logging

lastColor = None
lastMotorEAngle = None

def voltageCallback(value):
    print("Voltage: %s" % value)
    mqttc.publish("guitar/voltage", value)

def distanceCallback(distance):
    global lastColor
    if distance >= 6 and distance <= 8:
        lastColor = "YELLOW"
    elif distance >= 4 and distance <= 5:
        lastColor = "CYAN"
    elif distance >= 2 and distance <= 3:
        lastColor = "RED"
    elif distance >= 0 and distance <= 1:
        lastColor = "BLUE"
    else:
        lastColor = None

def motorACallback(angle):
    print("Motor A: %s" % angle)
    mqttc.publish("guitar/motor_a", angle)

def motorBCallback(angle):
    print("Motor B: %s" % angle)
    mqttc.publish("guitar/motor_b", angle)
    
def motorECallback(angle):
    global lastMotorEAngle
    print("Motor E: %s" % angle)
    pivot = 0
    if lastMotorEAngle is not None:
        if lastColor is not None:
            if (lastMotorEAngle < pivot and angle > pivot) or (lastMotorEAngle > pivot and angle < pivot):
                print(lastColor)
                mqttc.publish("guitar/color", lastColor)
    lastMotorEAngle = angle

def bumpCallback(count):
    print("Bump!")
    mqttc.publish("guitar/bump", 1)

#logging.basicConfig()
#logging.getLogger('pygatt').setLevel(logging.DEBUG)

print("Connecting to Mosquitto...")
mqttc = mqtt.Client()
mqttc.connect("localhost", 1883, 60)
mqttc.loop_start()

print("Searching for LEGO Move Hub...")

conn = BlueGigaConnection()
conn.connect()

try:
    hub = MoveHub(conn)

    print("Connected to LEGO Move Hub! Now subscribing...")

    hub.voltage.subscribe(voltageCallback)
    hub.color_distance_sensor.subscribe(distanceCallback, mode=ColorDistanceSensor.DISTANCE_INCHES)
    hub.motor_A.subscribe(motorACallback, mode=EncodedMotor.SENSOR_ANGLE)
    hub.motor_B.subscribe(motorBCallback, mode=EncodedMotor.SENSOR_ANGLE)
    hub.motor_external.subscribe(motorECallback, mode=EncodedMotor.SENSOR_ANGLE)
    hub.tilt_sensor.subscribe(bumpCallback, mode=TiltSensor.MODE_BUMP_COUNT)
    
    input("Press Enter to quit...")

finally:
    conn.disconnect()
    mqttc.loop_stop()
