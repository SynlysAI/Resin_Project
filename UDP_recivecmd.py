import socket
import threading


class UDPSignalReceiver:
    """
    UDP信号接收器类
    启动后会在子线程中持续监听UDP信号，当接收到指定信号时执行事件委托
    """
    
    def __init__(self, host='127.0.0.1', port=8888):
        """
        初始化UDP信号接收器
        
        :param host: 监听的主机地址
        :param port: 监听的端口
        """
        self.host = host
        self.port = port
        self.udp_socket = None
        self.listen_thread = None
        self.is_running = False
        # 事件委托，初始化为None
        self.on_receive_signal = None
        
    def start_listening(self):
        """
        启动UDP监听子线程
        """
        if not self.is_running:
            self.is_running = True
            # 创建UDP套接字
            self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # 绑定本地地址和端口
            local_addr = (self.host, self.port)
            self.udp_socket.bind(local_addr)
            
            # 启动子线程进行监听
            self.listen_thread = threading.Thread(target=self._listen_loop)
            self.listen_thread.daemon = True  # 设置为守护线程，主程序退出时自动结束
            self.listen_thread.start()
            print(f"UDP信号接收器已启动，监听 {self.host}:{self.port}")
    
    def _listen_loop(self):
        """
        UDP监听循环，在子线程中运行
        """
        try:
            while self.is_running:
                # 接收数据（缓冲区大小1024字节）
                data, sender_addr = self.udp_socket.recvfrom(1024)
                decoded_data = data.decode('utf-8')
                print(f"\n收到来自 {sender_addr} 的UDP消息：{decoded_data}")
                
                # 只有当接收到的消息是"OK"时才执行事件委托
                if decoded_data == "OK" and self.on_receive_signal is not None:
                    try:
                        self.on_receive_signal()  # 事件委托不再接收参数
                    except Exception as e:
                        print(f"执行事件委托时发生错误：{e}")
        except Exception as e:
            if self.is_running:  # 如果不是因为停止而产生的错误，则打印
                print(f"UDP监听发生错误：{e}")
    
    def stop_listening(self):
        """
        停止UDP监听
        """
        if self.is_running:
            self.is_running = False
            # 关闭套接字
            if self.udp_socket:
                self.udp_socket.close()
            # 等待子线程结束
            if self.listen_thread and self.listen_thread.is_alive():
                self.listen_thread.join(timeout=1.0)
            print("UDP信号接收器已停止")
    
    def set_signal_handler(self, handler):
        """
        设置UDP信号处理的事件委托
        
        :param handler: 处理函数，不接收任何参数
        """
        self.on_receive_signal = handler


# 示例用法
if __name__ == "__main__":
    # 创建UDP信号接收器实例
    udp_receiver = UDPSignalReceiver()
    
    # 定义信号处理函数
    def handle_received_signal():
        print("处理接收到的OK信号")
        # 这里可以添加具体的信号处理逻辑
    
    # 设置信号处理函数
    udp_receiver.set_signal_handler(handle_received_signal)
    
    try:
        # 启动监听
        udp_receiver.start_listening()
        print("按Ctrl+C停止UDP接收器...")
        
        # 主线程保持运行
        while True:
            pass
    except KeyboardInterrupt:
        print("\n收到停止信号")
    finally:
        # 停止监听
        udp_receiver.stop_listening()