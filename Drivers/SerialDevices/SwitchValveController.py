import time
from Drivers.SerialDevices.Common_Serial import Common_Serial

class SwitchValve:
    def __init__(self, serial_port: Common_Serial, address: int):
        self.serial_port = serial_port
        self.address = address


    def move_to_position(self, position: int):
        time.sleep(1)
        data = bytes([self.address, 0x05, 0x00, position,0xFF,0x00])
        recv = self.serial_port.sendcmd(data,8)
        time.sleep(2)
        # 读取一次位置直到到达目标
        pos = self.query_position()
        print(f'当前位置: {pos}, 目标位置: {position}')
        return pos == position


    def query_position(self):
        data = bytes([self.address, 0x04, 0x00,0x00, 0x00,0x02])
        recv=self.serial_port.sendcmd(data,9)
        if len(recv) == 9:
            # 返回数据格式: 地址 04 04 4C 00 00 XX CRC16
            value = int.from_bytes(recv[6:7], byteorder='big', signed=False)
            return value
        return None
