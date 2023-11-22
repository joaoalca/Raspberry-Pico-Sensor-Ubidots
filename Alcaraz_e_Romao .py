from umqtt.simple import MQTTClient
from machine import Pin
import machine
import utime
import network
gatilho = Pin(21, Pin.OUT)
eco = Pin(20, Pin.IN)
ssid = 'Inteli-COLLEGE'
password = 'QazWsx@123'
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)
while not wlan.isconnected():
    pass
print("Conectado. Endereço IP:", wlan.ifconfig()[0])
TOKEN = "BBUS-YmiIPOdUMNRVQj9fEPgZYqCS5K5PYa"
CLIENT_ID = "unique_id"
TOPIC = b"/v1.6/devices/alca-e-romao/sensor"
def connect_mqtt():
    client = MQTTClient(CLIENT_ID, "industrial.api.ubidots.com", user=TOKEN, password="")
    client.connect()
    return client
def publish(client, value):
    msg = b"%s" % value
    client.publish(TOPIC, msg)
client = connect_mqtt()
while True:
    gatilho.low()
    utime.sleep_us(2)
    gatilho.high()
    utime.sleep_us(10)
    gatilho.low()
    while eco.value() == 0:
        sinal_desligado = utime.ticks_us()
    while eco.value() == 1:
        sinal_ligado = utime.ticks_us()
    tempo_passado = sinal_ligado - sinal_desligado
    distancia = (tempo_passado * 0.0343) / 2
    print("A distância do objeto é ", distancia, "cm")
    publish(client, distancia)
    utime.sleep(5)







