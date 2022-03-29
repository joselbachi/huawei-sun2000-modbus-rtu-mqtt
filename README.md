# Huawei SUN2000 KTL L1 Inverter Modbus RTU to MQTT
Monitorizamos el inversor Huawei SUN2000L KTL L1 vía Modbus RTU  y publicamos los valores con MQTT

**What is this?**

En el repositorio original, el servidor MQTT no tiene usuario/contraseña.
Así mismo, envían los datos cada 1 segundo. 

He añadido tres variables para poder cambiarlo desde la configuración.

Usamos un fork de https://github.com/ccorderor/huawei-sun2000-modbus-rtu-mqtt que a su vez usa
una versión forked de la librería HuaweiSolar (https://gitlab.com/Emilv2/huawei-solar) de Emilv2. 

**Generar el container de docker**

Clonar el repositorio.

Desde el directorio clonado generamos la imagen de docker con:

```
docker build -t huawei-solar-rtu
```

Una vez generada la imagen, podemos usar el siguiente servicio docker-compose para iniciarlo:


```
 huawei-solar-rtu:
    container_name: huawei-solar-rtu
    restart: unless-stopped
    image: huawei-solar-rtu:latest
    user: root
    devices:
      - /dev/ttyUSB0:/dev/ttyUSB0
    environment:
      - INVERTER_PORT=/dev/ttyUSB0
      - MQTT_HOST=192.168.1.40
      - MQTT_USER=XXXXXXX
      - MQTT_PASS=PPPPPPP
      - WAIT_SLEEP=N (en segundos)
```
