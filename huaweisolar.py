import time
from base_solar import HuaweiSolar
import base_solar
import paho.mqtt.client
import os

import logging
FORMAT = ('%(asctime)-15s %(threadName)-15s '
          '%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.INFO)

inverter_port = os.getenv('INVERTER_PORT', '/dev/ttyUSB0')
mqtt_host = os.getenv('MQTT_HOST', '192.168.1.40')
mqtt_user = os.getenv('MQTT_USER', '')
mqtt_pass = os.getenv('MQTT_PASS', '')
wait_sleep = os.getenv('WAIT_SLEEP', '')

inverter = base_solar.HuaweiSolar(inverter_port, slave=1)
inverter._slave = 1
inverter.wait = wait_sleep

#vars = ['state_1','state_2', 'state_3', 'alarm_1', 'alarm_2', 'alarm_3', 'pv_01_voltage', 'pv_01_current', 'pv_02_voltage','pv_02_current', 'input_power', 'grid_voltage', 
#'grid_current', 'day_active_power_peak', 'active_power', 'reactive_power', 
#'grid_frequency', 'efficiency', 'internal_temperature', 'insulation_resistance', 'device_status', 'fault_code', 'startup_time', 'shutdown_time', 'accumulated_yield_energy',
#'daily_yield_energy', 'grid_A_voltage', 'active_grid_A_current', 'power_meter_active_power', 
#'grid_exported_energy', 'grid_accumulated_energy']

#vars = ['alarm_1', 'pv_01_voltage', 'pv_01_current', 'pv_02_voltage','pv_02_current', 'input_power', 'grid_voltage', 
#'grid_current', 'day_active_power_peak', 'active_power', 'reactive_power', 
#'grid_frequency', 'efficiency', 'internal_temperature', 'insulation_resistance', 'device_status', 'fault_code', 'startup_time', 'shutdown_time', 'accumulated_yield_energy',
#'daily_yield_energy', 'grid_A_voltage', 'active_grid_A_current', 'power_meter_active_power', 
#'grid_exported_energy', 'grid_accumulated_energy']


def modbusAccess():

    vars_inmediate = ['pv_01_voltage', 'pv_01_current', 'pv_02_voltage','pv_02_current', 'input_power', 'grid_voltage', 
    'grid_current', 'active_power', 
    'grid_A_voltage', 'active_grid_A_current', 'power_meter_active_power']

    vars = ['day_active_power_peak', 'efficiency', 'internal_temperature', 'insulation_resistance', 'device_status', 'fault_code', 'accumulated_yield_energy',
    'daily_yield_energy', 'grid_exported_energy', 'grid_accumulated_energy']

    cont = 0
    while True:

        for i in vars_inmediate:
            try:
                mid = inverter.get(i)
                log.debug(i)
                log.debug(mid)
                log.debug("---")

                clientMQTT.publish(topic="emon/NodeHuawei/"+i, payload= str(mid.value), qos=1, retain=False)
            except:
                pass

        if(cont > 0):
            for i in vars:
                try:
                    mid = inverter.get(i)
                    log.debug(i)
                    log.debug(mid)
                    log.debug("---")

                    clientMQTT.publish(topic="emon/NodeHuawei/"+i, payload= str(mid.value), qos=1, retain=False)
                except:
                    pass

            cont = 0

        cont = cont + 1   
        time.sleep(wait_sleep)





def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True #set flag
        log.info("MQTT OK!")
    else:
        log.info("MQTT FAILURE. ERROR CODE: %s",rc)


paho.mqtt.client.Client.connected_flag=False#create flag in class
broker_port = 1883

clientMQTT = paho.mqtt.client.Client()
clientMQTT.on_connect=on_connect #bind call back function
clientMQTT.loop_start()
log.info("Connecting to MQTT broker: %s ",mqtt_host)
clientMQTT.username_pw_set(mqtt_user,mqtt_pass)
clientMQTT.connect(mqtt_host, broker_port) #connect to broker
while not clientMQTT.connected_flag: #wait in loop
    log.info("...")
time.sleep(1)
log.info("START MODBUS...")

modbusAccess()

clientMQTT.loop_stop()
