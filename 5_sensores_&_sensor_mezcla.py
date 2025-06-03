from machine import Pin, time_pulse_us
import time

# Parámetros
ALTURA_TANQUE_CM = 12
UMBRAL_VACIO_PORC = 10
TRANSFERENCIA_PORC = 5

sensores = [
    {"color": "Cyan",    "trigger_pin": 3,  "echo_pin": 2,  "led_pin": 10, "aportado": 0},
    {"color": "Magenta", "trigger_pin": 5,  "echo_pin": 4,  "led_pin": 11, "aportado": 0},
    {"color": "Yellow",  "trigger_pin": 7,  "echo_pin": 6,  "led_pin": 12, "aportado": 0},
    {"color": "Black",   "trigger_pin": 9,  "echo_pin": 8,  "led_pin": 13, "aportado": 0},
    {"color": "White",   "trigger_pin": 11, "echo_pin": 10, "led_pin": 14, "aportado": 0},
]

mezcla = {
    "color": "Mezcla",
    "trigger_pin": 13,
    "echo_pin": 12,
    "led_pin": 15,
    "nivel": 0
}

def inicializar_sensor(sensor):
    sensor["trigger"] = Pin(sensor["trigger_pin"], Pin.OUT)
    sensor["echo"] = Pin(sensor["echo_pin"], Pin.IN)
    sensor["led"] = Pin(sensor["led_pin"], Pin.OUT)

for sensor in sensores:
    inicializar_sensor(sensor)

inicializar_sensor(mezcla)

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

def calcular_porcentaje(distancia):
    if distancia < 0 or distancia > ALTURA_TANQUE_CM:
        return 0
    return int(((ALTURA_TANQUE_CM - distancia) / ALTURA_TANQUE_CM) * 100)

# Bucle principal
while True:
    print("\n========== LECTURA Y TRANSFERENCIA ==========")

    mezcla_actual = medir_distancia(mezcla["trigger"], mezcla["echo"])
    mezcla["nivel"] = calcular_porcentaje(mezcla_actual)
    print(f"🧪 Mezcla - Nivel actual: {mezcla['nivel']}%")

    for sensor in sensores:
        color = sensor["color"]
        distancia = medir_distancia(sensor["trigger"], sensor["echo"])
        porcentaje = calcular_porcentaje(distancia)

        if distancia == -1:
            print(f" {color}: No se recibe señal del sensor.")
            sensor["led"].value(1)
        elif porcentaje <= UMBRAL_VACIO_PORC:
            print(f" {color}: Nivel bajo ({porcentaje}%). No se transfiere.")
            sensor["led"].value(1)
        elif mezcla["nivel"] >= 100:
            print(f" {color}: Mezcla llena. No se transfiere.")
            sensor["led"].value(1)
        else:
            transferido = min(TRANSFERENCIA_PORC, 100 - mezcla["nivel"])
            mezcla["nivel"] += transferido
            sensor["aportado"] += transferido
            print(f" {color}: Nivel = {porcentaje}% | Transfiere {transferido}%")
            sensor["led"].value(0)

        print("---------------------------------")

    print("Contribución a la mezcla:")
    for sensor in sensores:
        print(f"  - {sensor['color']}: {sensor['aportado']}%")
    print(f" Mezcla - Nivel total: {mezcla['nivel']}%")

    if mezcla["nivel"] >= 100:
        print("Mezcla completa. Proceso finalizado.")
        mezcla["led"].value(1)
    else:
        mezcla["led"].value(0)

    time.sleep(2)
