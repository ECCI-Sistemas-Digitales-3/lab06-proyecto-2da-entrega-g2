from machine import Pin, time_pulse_us
import time

# Parámetros del tanque
ALTURA_TANQUE_CM = 20
UMBRAL_VACIO_PORC = 10

# Lista de sensores con sus nombres, pines y color asociado
sensores = [
    {"color": "Cyan",    "trigger_pin": 3,  "echo_pin": 2,  "led_pin": 10},
    {"color": "Magenta", "trigger_pin": 5,  "echo_pin": 4,  "led_pin": 11},
    {"color": "Yellow",  "trigger_pin": 7,  "echo_pin": 6,  "led_pin": 12},
    {"color": "Black",   "trigger_pin": 9,  "echo_pin": 8,  "led_pin": 13},
    {"color": "White",   "trigger_pin": 11, "echo_pin": 10, "led_pin": 14},
]

# Inicialización de pines
for sensor in sensores:
    sensor["trigger"] = Pin(sensor["trigger_pin"], Pin.OUT)
    sensor["echo"] = Pin(sensor["echo_pin"], Pin.IN)
    sensor["led"] = Pin(sensor["led_pin"], Pin.OUT)

def medir_distancia(trigger, echo):
    trigger.low()
    time.sleep_us(2)
    trigger.high()
    time.sleep_us(10)
    trigger.low()

    try:
        duracion = time_pulse_us(echo, 1, 30000)
        if duracion < 0:
            return -1
    except OSError:
        return -1

    distancia = (duracion / 2) / 29.1
    return distancia

def calcular_porcentaje(distancia, altura_total):
    if distancia < 0 or distancia > altura_total:
        return 0
    return int(((altura_total - distancia) / altura_total) * 100)

# Bucle principal
while True:
    print("========== LECTURA DE SENSORES CMYK+W ==========")

    for sensor in sensores:
        color = sensor["color"]
        distancia = medir_distancia(sensor["trigger"], sensor["echo"])
        porcentaje = calcular_porcentaje(distancia, ALTURA_TANQUE_CM)

        if distancia == -1:
            print(f" {color}: No se recibe señal del sensor.")
            sensor["led"].value(1)
            distancia = 0
            porcentaje = 0
        else:
            print(f"{color}: Distancia = {distancia:.2f} cm | Nivel = {porcentaje}%")
            if porcentaje <= UMBRAL_VACIO_PORC:
                sensor["led"].value(1)
                print(f" {color}: Tanque vacío o con nivel bajo.")
            else:
                sensor["led"].value(0)
                print(f" {color}: Nivel adecuado.")

        print("-----------------------------------------")

    time.sleep(1)
