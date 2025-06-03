# Sistema de Monitoreo de Nivel de Pintura con 5 Sensores Ultrasónicos (CMYK + Blanco)

Este script está diseñado para ejecutarse en una **Raspberry Pi Pico** utilizando **MicroPython** desde **Thonny IDE**.
Permite leer 5 sensores ultrasónicos **SRF05** conectados a tanques de pintura que representan los colores del modelo **CMYK + Blanco**.
Si el nivel de un tanque es bajo o no se detecta señal, se enciende un LED de alerta.

Detalle de colores:
- C: Cyan
- M: Magenta
- Y: Yellow
- K: Black
- W: White

---

## Componentes requeridos para montaje

- Raspberry Pi Pico
- 5 sensores ultrasónicos SRF05
- 5 LEDs (uno por color)
- Resistencias para LEDs
- Divisores de voltaje en los pines `ECHO` (ya que SRF05 opera a 5V)
- Protoboard y cables

---

## Pines usados

| Color   | TRIG (GPIO) | ECHO (GPIO) | LED (GPIO) |
|---------|-------------|-------------|------------|
| Cyan    | GP3         | GP2         | GP10       |
| Magenta | GP5         | GP4         | GP11       |
| Yellow  | GP7         | GP6         | GP12       |
| Black   | GP9         | GP8         | GP13       |
| White   | GP17        | GP16        | GP14       |

---

## Descripción código

### Importamos librerias necesarias:

```python
from machine import Pin, time_pulse_us
import time
```
1. `from machine import Pin`: Esto permite controlar los pines GPIO (entradas/salidas digitales) del microcontrolador, para poder configurar un pin como entrada o salida.
2. `time_pulse_us`: Se utiliza para medir cuánto tiempo un pin permanece en un estado (alto o bajo)
3. `time`: Se usa para controlar pausas en la ejecución, medir tiempo, realizar retardos, etc.

### Datos del tanque

```python
ALTURA_TANQUE_CM = 12        
UMBRAL_VACIO_PORC = 10 
```
**Parámetros:**
- `ALTURA_TANQUE_CM`: Altura total del tanque en cm, se establece como parámetro al inicio para poder realizar los cálculos posteriormente.
- `UMBRAL_VACIO_PORC`: Se define un umbral de nivel mínimo para considerar el tanque como vacío, en este caso se define con un 10%.

### Definición de sensores por color, pines y salida de alerta:

```python
sensores = [
    {"color": "Cyan",    "trigger_pin": 3,  "echo_pin": 2,  "led_pin": 10},
    {"color": "Magenta", "trigger_pin": 5,  "echo_pin": 4,  "led_pin": 11},
    {"color": "Yellow",  "trigger_pin": 7,  "echo_pin": 6,  "led_pin": 12},
    {"color": "Black",   "trigger_pin": 9,  "echo_pin": 8,  "led_pin": 13},
    {"color": "White",   "trigger_pin": 11, "echo_pin": 10, "led_pin": 14},
]
```
Para cada sensor se le asigna directamente un respectivo color, para identificarlo en el código su respectivo porcentaje y lectura y así mismo su respectivos pines para la conexión física.

Adicionalmente, se declara un respectivo LED de advertencia para cada uno, con un pin de salida definido.

### Inicialización de sensores

Inicialización de los 5 sensores por medio de los pines trigger y echo, teniendo en cuenta que se configuró para sensores SRF05.
También se inicializan los pines correspondientes a los LEDs de cada sensor.

```python
for sensor in sensores:
    sensor["trigger"] = Pin(sensor["trigger_pin"], Pin.OUT)
    sensor["echo"] = Pin(sensor["echo_pin"], Pin.IN)
    sensor["led"] = Pin(sensor["led_pin"], Pin.OUT)
```

### Función `medir_distancia()`

Esta funcion sirve para medir la distancia que hay entre la pintura y el sensor ultrasónico.
```python
def medir_distancia(trigger, echo):
```
Dividiendo la función en las siguientes partes:

Generación de un pulso por medio del pin "trigger" del sensor ultrasónico, mandando una secuencia que confirma primero el estado en bajo del pin, luego lo pone en alto por 10 microsegundos y lo vuelve a bajar.
```python
    trigger.low()
    time.sleep_us(2)
    trigger.high()
    time.sleep_us(10)
    trigger.low()
```
El pulso enviado por medio del sensor se refleja y se detecta por este mismo, y con esto medimos el tiempo que este tarda en volver por medio del pin "echo" con la función `time_pulse_us`.
Posteriormente se corrobora el dato obtenido, por lo que si no se recibe señal entonces lo clasifica con un `-1`, esto debido a si el sensor no está conectado o así mismo para identificar si se está enviando señal.
```python
    try:
        duracion = time_pulse_us(echo, 1, 30000)
        if duracion < 0:
            return -1  # Sin señal
    except OSError:
        return -1      # Excepción si no se recibe eco
```
Posteriormente con el dato obtenido y guardado en la variable `duración`, se convierte el tiempo a distancia en centimetros(cm) y se guarda en la variable `distancia`.

La variable `duración` se divide entre dos por lo que el tiempo que registra el sensor es tras la señal ir y volver (`duracion / 2`).

La conversión de tiempo en microsegundos a distancia en centimetros se realiza con la relación de la velocidad del sonido en el aire (`(duracion / 2) / 29.1`).
```python
    distancia = (duracion / 2) / 29.1
    return distancia
```

### Función `calcular_porcentaje()`
Teniendo la distancia de la función `medir_distancia()`, se realiza el cálculo del porcentaje que esto representa en el tanque, teniendo en cuenta la distancia total del tanque definida en el parámetro `ALTURA_TANQUE_CM`.
- Si la distancia es menor que `0` o mayor que la altura del tanque devuelve un "0", esto para poder filtrar los datos erroneos o fuera de rango.
- Si no aplica la condición anterior, entonces la función retorna el porcentaje respectivo.
```python
def calcular_porcentaje(distancia, altura_total):
    if distancia < 0 or distancia > altura_total:
        return 0
    return int(((altura_total - distancia) / altura_total) * 100)
```

### Bucle Principal:
El bucle principal del código que usa lo demás que se ha definido y calculado hasta el momento se ejecuta mostrando en la consola de Thonny la lectura en tiempo real de los sensores.

Para ello se realizan los siguientes pasos:
- Iteración por cada sensor para ir revisando cada uno de los sensores definidos del CMYK+W, por lo que recorre los sensores uno por uno y se calcula la distancia y el porcentaje.
```python
while True:
    print("========== LECTURA DE SENSORES CMYK+W ==========")

    for sensor in sensores:
        color = sensor["color"]
        distancia = medir_distancia(sensor["trigger"], sensor["echo"])
        porcentaje = calcular_porcentaje(distancia, ALTURA_TANQUE_CM)
```
- En la misma iteración se evalua si no se recibió señal: asignando las variables `distancia` y `porcentaje` en "0" y a su vez mostrando en pantalla mensaje respectivo `f" {color}: No se recibe señal del sensor.`.
```python
        if distancia == -1:
            print(f" {color}: No se recibe señal del sensor.")
            sensor["led"].value(1)
            distancia = 0
            porcentaje = 0
```
- Si por el contrario se recibe señal, se muestra la distancia medida y el porcentaje del tanque:
```python
        else:
            print(f"{color}: Distancia = {distancia:.2f} cm | Nivel = {porcentaje}%")
```
- Después, se valida si cuenta con el nivel suficiente de pintura por encima del porcentaje definido en el parámetro `UMBRAL_VACIO_PORC`.
- Si el nivel es bajo: Se activa alerta por led (`sensor["led"].value(1)`) y por mensaje en consola (`print(f" {color}: Tanque vacío o con nivel bajo.")`).
```python
            if porcentaje <= UMBRAL_VACIO_PORC:
                sensor["led"].value(1)
                print(f" {color}: Tanque vacío o con nivel bajo.")
```
- Si el nivel se encuentra dentro del rango: El led se mantiene apagado (`sensor["led"].value(0)`) y se muestra el mensaje "`f" {color}: Nivel adecuado.`".
```python
            else:
                sensor["led"].value(0)
                print(f" {color}: Nivel adecuado.")

        print("-----------------------------------------")
```
- Por último, se hace una espera de un segundo antes de volver a leer el sensor y repetir el proceso.
```python
    time.sleep(1)
```
