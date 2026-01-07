from BusinessActions.DeviceManager import DeviceManager
from Drivers.SerialDevices.TemperatureController import TemperatureController

def TemperatureControl_set_temperature(temperature_control:TemperatureController,temperature:float):
    temperature_control.set_temperature(temperature)

def TemperatureControl_read_temperature(temperature_control:TemperatureController):
    return temperature_control.read_temperature()

def Temp_set(device_manager:DeviceManager,reactor_id:int,temperature:float):
    if device_manager.temp_sensors:
        temp_controller = device_manager.temp_sensors[reactor_id-1]# 索引从0开始，reactor_id从1开始
        temp_controller.set_temperature(temperature)
    
