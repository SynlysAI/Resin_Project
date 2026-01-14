import serial
import threading
import time

class Common_Serial:
    def __init__(self, com_port):
        self.ser = serial.Serial(
            port=com_port,
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=1
        )
        self.lock=threading.Lock()
        print(f"Common_Serial initialized on port {com_port}")

    def crc16(self, data: bytes) -> bytes:
        crc = 0xFFFF
        for pos in data:
            crc ^= pos
            for _ in range(8):
                if (crc & 0x0001) != 0:
                    crc >>= 1
                    crc ^= 0xA001
                else:
                    crc >>= 1
        crc_low = crc & 0xFF
        crc_high = (crc >> 8) & 0xFF
        return data + bytes([crc_low, crc_high])
    
    def sendcmd(self,cmd:bytes,res_len:int):
        #必须使用锁确保线程安全，确保收到信息之前不会发送其他信息
        with self.lock:
            packet = self.crc16(cmd)
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()
            print('发送数据:', packet.hex(' ').upper())
            self.ser.write(packet)
            recv = self.ser.read(res_len)
            print('接收数据:', recv.hex(' ').upper())
            return recv

    def disconnect(self):
        self.ser.close()
        print("Serial port disconnected")

# 确保类能被外部访问
print("模块内容:", dir())