import re
import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("guitar/+")

def on_message(client, userdata, msg):
    match = re.match("guitar/([^/]+)", msg.topic)
    event_type = match.group(1)
    event_tags = None

    if event_type == "voltage":
        event_payload = float(msg.payload)
    elif event_type == "bump":
        event_payload = int(msg.payload)
    elif event_type == "color":
        event_payload = 1
        event_tags = {
            "color": msg.payload.decode()
        }
    elif event_type == "motor_a":
        event_type = "motor"
        event_payload = int(msg.payload)
        event_tags = {
            "motor": "A"
        }
    elif event_type == "motor_b":
        event_type = "motor"
        event_payload = int(msg.payload)
        event_tags = {
            "motor": "B"
        }
    else:
        event_type = None

    if event_type is not None:
        send_to_influxdb(event_type, event_tags, event_payload)

def send_to_influxdb(type, tags, payload):
    json_body = [
        {
            "measurement": type,
            "fields": {
                "value": payload
            }
        }
    ]
    if tags is not None:
        json_body[0]["tags"] = tags
    print(json_body)
    influxdb_client.write_points(json_body)

def switch_influxdb(db):
    databases = influxdb_client.get_list_database()
    if len(list(filter(lambda x: x["name"] == db, databases))) == 0:
        print("Creating InfluxDB database " + db)
        influxdb_client.create_database(db)
    print("Using InfluxDB database " + db)
    influxdb_client.switch_database(db)

print("Connecting to InfluxDB...")
influxdb_client = InfluxDBClient("localhost", 8086)
switch_influxdb("guitar")

print("Connecting to Mosquitto...")
mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.connect("localhost", 1883)

mqttc.loop_forever()
