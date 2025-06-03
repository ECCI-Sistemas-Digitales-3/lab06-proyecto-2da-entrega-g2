[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=19621453&assignment_repo_type=AssignmentRepo)
# Lab06: Proyecto 2da. entrega

## Integrantes
- [Daniel Ricardo Roa](https://github.com/DRRR555)
- [Germán Moreno Calderón](https://github.com/GerHub-blip)
- [Christian Camilo Caicedo Peña](https://github.com/ChristianCCaicedoP)
  
# Códigos Implementados
En el proyecto integrador se hace uso de sensores ultrasonido para poder revisar la cantidad de pintura que hay en cada tanque, siendo estos cada uno de los colores que componen el CMYK (Cyan, Magenta, Yellow, Black) más el Blanco, por ello da un total de 5 tanques de colores base que se mezclan para poder obtener como resultado el color deseado en un último tanque, este también cuenta con su sensor respectivo para verificar el nivel.

Para la implementación de los sensores se realizaron códigos en micropython para poder integrarlos en node-red, de esta forma poder realizar el control de los niveles de cada tanque, mostrando el porcentaje en que se encuentra cada uno y así ayudando a identificar si cuenta con suficiente pintura para realizar la mezcla o mostrando una alerta deque el tanque se encuentra vacío o no recibe señal.

## Código 1, Implementación de 1 sensor Ultrasonido
Código identificado por nombre "[1_Sensor_Probado](https://github.com/ECCI-Sistemas-Digitales-3/lab06-proyecto-2da-entrega-g2/blob/af7a38a30919af737fd60ace09a22fc8ea263fd5/1_Sensor_Probado.py)".

En este código se realiza la implementación de un sensor ultrasonido el cual se conecta a una fuente de 5 Voltios, resistencias de protección y a la Raspberry Pi Pico, la cual recibe la señal del sensor y la analiza para poder mostrar el valor del porcentaje en el que el tanque se encuentra; de la Raspberry se utilizaron pines para poder lnelazar los diferentes componentes, por ello en el siguiente archivo se puede apreciar los pines que se asignaron y la conexión con el sensor y con un led de advertencia: "[In_Out_1_Sensor_Probado](https://github.com/ECCI-Sistemas-Digitales-3/lab06-proyecto-2da-entrega-g2/blob/af7a38a30919af737fd60ace09a22fc8ea263fd5/In_Out_1_Sensor_Probado.txt)".

Este código se probó el funcionamiento obteniendo un satisfactorio resultado, para ello se muestra prueba de ello en este [Video](https://youtube.com/shorts/C4vVS9Mlb_U?feature=share).


## Código 2, Implementación de 5 sensores simultaneos
Para el código identificado por nombre "[5_Sensores](https://github.com/ECCI-Sistemas-Digitales-3/lab06-proyecto-2da-entrega-g2/blob/af7a38a30919af737fd60ace09a22fc8ea263fd5/5_sensores.py)".

Tomando en cuenta el primer código donde se implementó un sensor de ultrasonido, se modifica y se añaden 4 sensores para un total de 5 siendo 1 por tanque, de esta forma se parte desde un código que ya se confirmó su correcto funcionamiento y se adapta al proyecto integrador. Siguiendo la lógica del primer código implementado, se desarrolla el diagrama de flujo teniendo en cuenta la adición de los demás sensores [Diagrama_flujo](https://github.com/ECCI-Sistemas-Digitales-3/lab06-proyecto-2da-entrega-g2/blob/ba4990d18dcaff79a994d7deb597944296226b2c/Diagrama_flujo.md).

Adicionalmente, la descripción del código donde se desglosa y se evidencia cada parte de su funcionamiento se encuentra en el siguiente archivo "[Descripción_código_5_sensores](https://github.com/ECCI-Sistemas-Digitales-3/lab06-proyecto-2da-entrega-g2/blob/ba4990d18dcaff79a994d7deb597944296226b2c/Descripci%C3%B3n_c%C3%B3digo_5_sensores.md)"; así como el detalle de los pines utilizados y de los mensajes de advertencia que muestra el código "[In_Out_5_Sensores](https://github.com/ECCI-Sistemas-Digitales-3/lab06-proyecto-2da-entrega-g2/blob/af7a38a30919af737fd60ace09a22fc8ea263fd5/In_Out_5_Sensores.txt)".
