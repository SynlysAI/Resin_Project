from PySide6.QtWidgets import QApplication
from UIInteraction.UIGenerator.MainUI import MainUI
from UIInteraction.ControlActions.InputActionManager import InputActionManager
from BusinessActions.DeviceManager import DeviceManager
from PySide6.QtWidgets import QApplication, QPushButton
from PySide6.QtCore import QTimer, Qt
import sys
from UIInteraction.ControlActions.ButtonActionManager import ButtonActionManager
from UIInteraction.ParameterManagement.ParameterStorage import ParameterStorage
from BusinessActions.UIFeedback.UIFeedbackHandler import UIFeedbackHandler
from UIInteraction.ControlActions.DisplayActionManager import DisplayActionManager
from UIInteraction.RealTimeUpdate.RealTimeUpdate import RealTimeUpdate
from UDP_recivecmd import UDPSignalReceiver
from ActionSequence.execute_sequence import Import_Process_UDP

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
    udp_receiver = UDPSignalReceiver()
    # 设置信号处理函数
    udp_receiver.set_signal_handler(lambda :Import_Process_UDP(main_window.table_process))
    # 启动监听
    udp_receiver.start_listening()

    # 运行应用程序主循环
    sys.exit(app.exec())