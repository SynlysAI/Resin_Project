import json
import socket
import threading
import time
import os
from datetime import datetime


class TestUDPServer:
    """
    UDP测试服务器，用于测试ResinWorkstation
    """
    
    def __init__(self, host='127.0.0.1', port=9997, log_file='./logs/udp_server_log.json'):
        """
        初始化UDP测试服务器
        
        Args:
            host: 服务器主机地址
            port: 服务器端口
            log_file: 日志文件路径
        """
        self.host = host
        self.port = port
        self.log_file = log_file
        self.socket = None
        self.running = False
        self.thread = None
        self.log_data = []
        
        # 模拟设备状态
        self.device_state = {
            "connected": True,
            "operation_mode": "local",
            "device_status": "idle",
            "error_message": "",
            "solution_add_status": "idle",
            "current_solution_id": 0,
            "current_volume": 0.0,
            "target_volume": 0.0,
            "current_reactor_id": 0,
            "reactors": {
                1: {
                    "reactor_id": 1,
                    "current_temperature": 25.0,
                    "target_temperature": 25.0,
                    "stirring_status": False,
                    "stirring_speed": 0.0,
                    "n2_status": False,
                    "air_status": False,
                    "status": "idle",
                    "error_message": ""
                }
            },
            "post_processes": {
                1: {
                    "post_process_id": 1,
                    "cleaning_status": False,
                    "discharge_status": False,
                    "transferring_status": False,
                    "start_bottle": "",
                    "end_bottle": "",
                    "current_volume": 0.0,
                    "target_volume": 0.0,
                    "status": "idle",
                    "error_message": ""
                }
            }
        }
    
    def start(self):
        """
        启动UDP服务器
        """
        try:
            # 创建UDP socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.bind((self.host, self.port))
            self.running = True
            
            # 启动服务器线程
            self.thread = threading.Thread(target=self._server_loop, daemon=True)
            self.thread.start()
            
            print(f"UDP测试服务器已启动，监听 {self.host}:{self.port}")
            print(f"日志文件: {self.log_file}")
            print("按 Ctrl+C 停止服务器")
            return True
            
        except Exception as e:
            print(f"启动UDP服务器失败: {e}")
            return False
    
    def stop(self):
        """
        停止UDP服务器
        """
        self.running = False
        if self.socket:
            self.socket.close()
        if self.thread:
            self.thread.join()
        
        # 保存日志数据
        self._save_log()
        print("\nUDP服务器已停止")
    
    def _server_loop(self):
        """
        服务器主循环
        """
        while self.running:
            try:
                # 设置超时，以便定期检查running状态
                self.socket.settimeout(0.5)
                
                # 接收数据
                data, addr = self.socket.recvfrom(1024)
                client_ip, client_port = addr
                
                # 解析请求
                request = json.loads(data.decode('utf-8'))
                command = request.get('command', '')
                params = request.get('params', {})
                
                # 记录请求
                log_entry = {
                    "timestamp": datetime.now().isoformat(),
                    "client": f"{client_ip}:{client_port}",
                    "request": request,
                    "response": None
                }
                
                print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]")
                print(f"接收到命令: {command}")
                print(f"参数: {params}")
                
                # 处理命令
                response = self._handle_command(command, params)
                log_entry["response"] = response
                
                # 发送响应 - 明确标识为命令响应
                response_data = json.dumps(response).encode('utf-8')
                self.socket.sendto(response_data, addr)
                
                # 模拟发送一个状态更新（仅用于演示，实际环境中根据需要发送）
                # status_update = {
                #     "type": "status_update",
                #     "data": self.device_state
                # }
                # self.socket.sendto(json.dumps(status_update).encode('utf-8'), addr)
                
                print(f"发送响应: {response}")
                
                # 更新日志
                self.log_data.append(log_entry)
                
                # 每处理1条命令就保存日志（方法1）
                if len(self.log_data) % 1 == 0:
                    self._save_log()
                    
            except socket.timeout:
                continue
            except json.JSONDecodeError as e:
                print(f"JSON解析错误: {e}")
                error_response = {"status": "error", "message": "Invalid JSON format"}
                self.socket.sendto(json.dumps(error_response).encode('utf-8'), addr)
            except Exception as e:
                print(f"服务器错误: {e}")
    
    def _handle_command(self, command, params):
        """
        处理命令
        
        Args:
            command: 命令名称
            params: 命令参数
            
        Returns:
            dict: 响应数据
        """
        # 默认响应
        default_response = {"status": "success", "message": "Command executed successfully"}
        
        # 根据命令类型处理
        if command == "GET_DEVICE_STATE":
            return {"status": "success", "data": self.device_state}
        
        elif command == "GET_REACTOR_STATE":
            reactor_id = params.get("reactor_id", 1)
            reactor_state = self.device_state["reactors"].get(reactor_id, {})
            return {"status": "success", "data": reactor_state}
        
        elif command == "GET_POST_PROCESS_STATE":
            post_process_id = params.get("post_process_id", 1)
            post_process_state = self.device_state["post_processes"].get(post_process_id, {})
            return {"status": "success", "data": post_process_state}
        
        elif command == "TOGGLE_LOCAL_REMOTE_CONTROL":
            mode = params.get("mode", "local")
            if mode in ["local", "remote"]:
                self.device_state["operation_mode"] = mode
                return default_response
            else:
                return {"status": "error", "message": "Invalid mode"}
        
        elif command == "REACTOR_SOLUTION_ADD":
            # 模拟添加溶液
            solution_id = params.get("solution_id", 0)
            volume = params.get("volume", 0.0)
            reactor_id = params.get("reactor_id", 1)
            
            # 更新模拟状态
            self.device_state["solution_add_status"] = "completed"
            self.device_state["current_solution_id"] = solution_id
            self.device_state["current_volume"] = volume
            self.device_state["target_volume"] = volume
            self.device_state["current_reactor_id"] = reactor_id
            
            return default_response
        
        elif command == "POST_PROCESS_SOLUTION_ADD":
            # 模拟后处理溶液转移
            start_bottle = params.get("start_bottle", "")
            end_bottle = params.get("end_bottle", "")
            volume = params.get("volume", 0.0)
            
            # 更新模拟状态
            self.device_state["post_processes"][1]["transferring_status"] = False
            self.device_state["post_processes"][1]["start_bottle"] = start_bottle
            self.device_state["post_processes"][1]["end_bottle"] = end_bottle
            self.device_state["post_processes"][1]["current_volume"] = volume
            self.device_state["post_processes"][1]["target_volume"] = volume
            
            return default_response
        
        elif command == "POST_PROCESS_CLEAN":
            # 模拟后处理清洗
            post_process_id = params.get("post_process_id", 1)
            self.device_state["post_processes"][post_process_id]["cleaning_status"] = True
            return default_response
        
        elif command in ["REACTOR_N2_ON", "REACTOR_N2_OFF"]:
            # 模拟氮气控制
            reactor_id = params.get("reactor_id", 1)
            status = command == "REACTOR_N2_ON"
            self.device_state["reactors"][reactor_id]["n2_status"] = status
            return default_response
        
        elif command in ["REACTOR_AIR_ON", "REACTOR_AIR_OFF"]:
            # 模拟空气控制
            reactor_id = params.get("reactor_id", 1)
            status = command == "REACTOR_AIR_ON"
            self.device_state["reactors"][reactor_id]["air_status"] = status
            return default_response
        
        elif command == "TEMP_SET":
            # 模拟温度设置
            reactor_id = params.get("reactor_id", 1)
            temperature = params.get("temperature", 25.0)
            self.device_state["reactors"][reactor_id]["target_temperature"] = temperature
            # 模拟温度逐渐接近目标值
            self.device_state["reactors"][reactor_id]["current_temperature"] = temperature
            return default_response
        
        elif command == "START_STIR":
            # 模拟启动搅拌器
            reactor_id = params.get("reactor_id", 1)
            speed = params.get("speed", 0.0)
            self.device_state["reactors"][reactor_id]["stirring_status"] = True
            self.device_state["reactors"][reactor_id]["stirring_speed"] = speed
            return default_response
        
        elif command == "STOP_STIR":
            # 模拟停止搅拌器
            reactor_id = params.get("reactor_id", 1)
            self.device_state["reactors"][reactor_id]["stirring_status"] = False
            self.device_state["reactors"][reactor_id]["stirring_speed"] = 0.0
            return default_response
        
        elif command in ["POST_PROCESS_DISCHARGE_ON", "POST_PROCESS_DISCHARGE_OFF"]:
            # 模拟后处理排液控制
            post_process_id = params.get("post_process_id", 1)
            status = command == "POST_PROCESS_DISCHARGE_ON"
            self.device_state["post_processes"][post_process_id]["discharge_status"] = status
            return default_response
        
        else:
            # 未知命令
            return {"status": "success", "message": f"Unknown command: {command}"}
    
    def _save_log(self):
        """
        保存日志数据到文件
        """
        try:
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(self.log_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存日志失败: {e}")
    
    def _print_status(self):
        """
        打印服务器状态
        """
        print(f"\n服务器状态: 运行中")
        print(f"监听地址: {self.host}:{self.port}")
        print(f"处理命令数: {len(self.log_data)}")
        print(f"当前设备状态:")
        print(f"  - 操作模式: {self.device_state['operation_mode']}")
        print(f"  - 设备状态: {self.device_state['device_status']}")
        print(f"  - 反应器1温度: {self.device_state['reactors'][1]['current_temperature']}°C")
        print(f"  - 反应器1搅拌: {'运行中' if self.device_state['reactors'][1]['stirring_status'] else '停止'}")


def main():
    """
    主函数
    """
    # 创建并启动服务器
    server = TestUDPServer()
    if server.start():
        try:
            # 主循环，定期打印状态
            while True:
                time.sleep(5)
                server._print_status()
        except KeyboardInterrupt:
            # 捕获Ctrl+C，优雅停止服务器
            server.stop()


if __name__ == '__main__':
    main()