from UIInteraction.UIGenerator.MainUI import MainUI
import json
import socket
import sys

from PySide6.QtWidgets import QApplication

from ActionSequence.execute_sequence import Import_Process_UDP, Import_Parament_UDP
from BusinessActions.DeviceManager import DeviceManager
from BusinessActions.UIFeedback.UIFeedbackHandler import UIFeedbackHandler
from UDP_recivecmd import UDPSignalReceiver
from UIInteraction.ControlActions.ButtonActionManager import ButtonActionManager
from UIInteraction.ControlActions.DisplayActionManager import DisplayActionManager
from UIInteraction.ControlActions.InputActionManager import InputActionManager
from UIInteraction.ParameterManagement.ParameterStorage import ParameterStorage
from UIInteraction.RealTimeUpdate.RealTimeUpdate import RealTimeUpdate
from UIInteraction.UIGenerator.MainUI import MainUI


def send_udp_response(host, port, message):
    """
    发送UDP响应消息
    
    :param host: 目标主机地址
    :param port: 目标端口
    :param message: 要发送的消息字典
    """
    try:
        # 创建UDP套接字
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # 将消息转换为JSON字符串并编码
        json_message = json.dumps(message, ensure_ascii=False)
        udp_socket.sendto(json_message.encode('utf-8'), (host, port))
        print(f"✅ 已发送UDP响应到 {host}:{port}: {json_message}")

        # 关闭套接字
        udp_socket.close()
        return True
    except Exception as e:
        print(f"❌ 发送UDP响应失败: {e}")
        return False

if __name__ == "__main__":
    # 创建应用程序实例
    app = QApplication(sys.argv)

    # 创建MainUI实例
    main_window = MainUI()
    # 实例化UI反馈处理器
    ui_feedback = UIFeedbackHandler(main_window)
    #实例化参数管理器
    param_storage = ParameterStorage()

    device_manager = DeviceManager(param_storage)
    # 实例化输入管理器，验证输入限制效果
    input_manager = InputActionManager(main_window,param_storage)
    # 实例化按钮控件管理器
    button_manager = ButtonActionManager(main_window,device_manager,param_storage,ui_feedback)
    # 实例化显示动作管理器
    display_manager = DisplayActionManager(main_window, param_storage, button_manager)
    # 实例化实时更新实例
    real_time_update = RealTimeUpdate(device_manager,param_storage)

    # 设置窗口标题
    main_window.setWindowTitle("项目软件主界面")

    # 显示窗口
    main_window.show()
    # 建立udp监听
    udp_receiver = UDPSignalReceiver(host="127.0.0.1", port=8888)
    # 设置信号处理函数
    udp_receiver.set_signal_handler(lambda :Import_Process_UDP(main_window.table_process))
    # 启动监听
    udp_receiver.start_listening()
    #建立第二个UDP监听线程
    udp_receiver2 = UDPSignalReceiver(host="127.0.0.1", port=8889)
    # 创建一个闭包函数，预先设定send_udp_response的参数
    def create_response_sender():
        def send_response(message=None):
            if message is None:
                # 如果没有提供消息，发送默认响应
                return send_udp_response("127.0.0.1", udp_receiver2.back_port, {"status": "success"})
            else:
                # 如果提供了消息，直接发送该消息
                return send_udp_response("127.0.0.1", udp_receiver2.back_port, message)
        return send_response

    # 获取预先设定了参数的闭包函数
    response_sender = create_response_sender()
    # 设置信号处理函数，传递闭包函数作为参数
    udp_receiver2.set_signal_handler(lambda message=None:Import_Parament_UDP(message, device_manager, response_sender))
    # 启动监听
    udp_receiver2.start_listening()

    # 运行应用程序主循环
    sys.exit(app.exec())