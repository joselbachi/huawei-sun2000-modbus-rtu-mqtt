# Huawei SUN2000 KTL L1 Inverter Modbus RTU to MQTT
Monitorizamos el inversor Huawei SUN2000L KTL L1 vía Modbus RTU  y publicamos los valores con MQTT

**What is this?**

Usamos un fork de https://github.com/ccorderor/huawei-sun2000-modbus-rtu-mqtt que a su vez usa
una versión forked de la librería HuaweiSolar (https://gitlab.com/Emilv2/huawei-solar) de Emilv2. 

**Generar el container de docker**

First, download the code from this repo (you can either clone the repo or download the gzip file and extract it). You should download it in the same computer you are going to run the container.

Then, you need to generate the docker image. Enter inside the code folder, and execute the following command:

```
docker build -t huawei-solar-rtu
```

Once the docker image has been generated, you can use the following docker-compose service to initialize it:


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
      - MQTT_HOST=192.168.1.15
      - MQTT_USER=XXXXXXX
      - MQTT_PASS=PPPPPPP
      - WAIT_SLEEP=N (en segundos)
```
