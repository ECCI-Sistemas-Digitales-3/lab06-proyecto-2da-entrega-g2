from machine import Pin, time_pulse_us
import time

# Configuración inicial
TRIGGER_PIN = 3
ECHO_PIN = 2
LED_ALERTA_PIN = 15

trigger = Pin(TRIGGER_PIN, Pin.OUT)
echo = Pin(ECHO_PIN, Pin.IN)
led_alerta = Pin(LED_ALERTA_PIN, Pin.OUT)

ALTURA_TANQUE_CM = 12
UMBRAL_VACIO_PORC = 10

def medir_distancia_cm():
    # Enviar pulso ultrasónico
    trigger.low()
    time.sleep_us(2)
    trigger.high()
    time.sleep_us(10)
    trigger.low()
    
    duracion = time_pulse_us(echo, 1, 30000)
    
    if duracion < 0:
        return -1
    distancia_cm = (duracion / 2) / 29.1
    return distancia_cm

def calcular_porcentaje(distancia, altura_total):
    if distancia > altura_total:
        return 0
    elif distancia < 0:
        return -1
    else:
        return int(((altura_total - distancia) / altura_total) * 100)

# Bucle principal
while True:
    distancia = medir_distancia_cm()
    
    if distancia == -1:
        print("Error en la medición")
        led_alerta.value(1)
    else:
        porcentaje = calcular_porcentaje(distancia, ALTURA_TANQUE_CM)
        
        print("Distancia medida: {:.2f} cm".format(distancia))
        print("Nivel del tanque: {}%".format(porcentaje))
        
        if porcentaje <= UMBRAL_VACIO_PORC:
            led_alerta.value(1)
            print("Tanque vacío o casi vacío. No se puede continuar el proceso.")
        else:
            led_alerta.value(0)
            print("Tanque con suficiente pintura.")

    print("----------------------------")
    time.sleep(1)
