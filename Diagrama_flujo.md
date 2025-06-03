```mermaid
flowchart TD
    A[Inicio del programa] --> B[Inicializar pines TRIG, ECHO y LED por sensor]
    B --> C[Comenzar bucle de monitoreo]
    C --> D{¿Quedan sensores por leer?}
    
    D -- Sí --> E[Enviar pulso TRIG de 10us]
    E --> F[Esperar señal en ECHO con timeout]
    F --> G{¿Se recibió señal?}

    G -- Sí --> H[Calcular distancia y % de llenado]
    H --> I{¿% de llenado ≤ 10%?}
    I -- Sí --> J[Encender LED de alerta\nMostrar Tanque vacío]
    I -- No --> K[Mostrar % de llenado]

    G -- No --> L[Mostrar No se recibe señal \nAsignar 0%]
    L --> M[Encender LED de alerta]

    J --> N[Pasar al siguiente sensor]
    K --> N
    M --> N

    N --> D
    D -- No --> O[Esperar 1 segundo]
    O --> C
