from datetime import date
import time
from Drivers.SerialDevices.Common_Serial import Common_Serial

class Motor_Bottom:
    def __init__(self, serial_port: Common_Serial, address: int):
        self.serial_port = serial_port
        self.address = address

    def Run(self):
        # 启动电机
        data = bytes([self.address, 0xF6, 0x01,0x01,0xF4,0x00,0x00,0x6B])
        self.serial_port.ser.reset_input_buffer()
        self.serial_port.ser.reset_output_buffer()
        print('发送数据:', data.hex(' ').upper())
        self.serial_port.ser.write(data)
        recv = self.serial_port.ser.read(4)
        print('接收数据:', recv.hex(' ').upper())

    def stop(self):
        # 停止电机
        data = bytes([self.address, 0xFE,0x98,0x00,0x6B])
        self.serial_port.ser.reset_input_buffer()
        self.serial_port.ser.reset_output_buffer()
        print('发送数据:', data.hex(' ').upper())
        self.serial_port.ser.write(data)
        recv = self.serial_port.ser.read(4)
        print('接收数据:', recv.hex(' ').upper())
