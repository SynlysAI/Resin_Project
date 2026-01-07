from UIInteraction.UIGenerator.MainUI import MainUI
import serial.tools.list_ports
from PySide6.QtWidgets import QComboBox, QMessageBox, QPushButton
from BusinessActions.SingleStepActions.MotorAction import *
from BusinessActions.SingleStepActions.TemperatureControlAction import *
from BusinessActions.SingleStepActions.ValveAction import *
from BusinessActions.MultiStepActions.MultiStepActionManager import *
from BusinessActions.DeviceManager import DeviceManager
from UIInteraction.ParameterManagement.ParameterStorage import ParameterStorage
from BusinessActions.UIFeedback.UIFeedbackHandler import UIFeedbackHandler
from ActionSequence.execute_sequence import *
from BusinessActions.SingleStepActions.AxisSingleStepAction import *

class ButtonActionManager:
    """按钮控件管理器类，用于管理和处理所有按钮的事件"""
    
    def __init__(self, main_window:MainUI,device_manager:DeviceManager,param_storage:ParameterStorage,ui_feedback:UIFeedbackHandler):
        """初始化按钮控件管理器类
        
        Args:
            main_window (QMainWindow): 主窗口实例，用于访问和操作UI元素
        """
        self.main_window = main_window
        self.device_manager=device_manager
        self.param_storage=param_storage
        self.ui_feedback=ui_feedback
        self.setup_button_connections()
    
    def setup_button_connections(self):
        """设置所有按钮的信号槽连接"""
        # 连接刷新串口按钮的点击信号
        self.main_window.btn_refresh_port.clicked.connect(lambda: self.refresh_serial_ports(self.main_window.combo_port))
        self.main_window.btn_refresh_port_post.clicked.connect(lambda: self.refresh_serial_ports(self.main_window.combo_port_post))
       
        
        self.main_window.btn_connect.clicked.connect(self.device_manager.connnect_reactor_moudle)
        self.main_window.btn_connect_post.clicked.connect(self.device_manager.connect_post_module)
        self.main_window.btn_disconnect.clicked.connect(self.device_manager.disconnect_all_reactor_devices)
        self.main_window.btn_disconnect_post.clicked.connect(self.device_manager.disconnect_all_post_devices)
        self.main_window.btn_start_motor.clicked.connect(lambda :Motor_zmc_start_stirrer(self.device_manager.current_motorzmc,self.param_storage.set_motor_speed))
        self.main_window.btn_stop_motor.clicked.connect(lambda :Motor_zmc_stop_stirrer(self.device_manager.current_motorzmc))
        self.main_window.btn_start_bottom_motor.clicked.connect(lambda :Motor_Bottom_start_stirrer(self.device_manager.current_motor485_bottom))
        self.main_window.btn_stop_bottom_motor.clicked.connect(lambda :Motor_Bottom_stop_stirrer(self.device_manager.current_motor485_bottom))

        self.main_window.btn_temp_set.clicked.connect(lambda :TemperatureControl_set_temperature(self.device_manager.current_temp_sensor,self.param_storage.set_temperature))
        self.main_window.btn_start_motor_post.clicked.connect(lambda :Motor_485_idm42_start_stirrer(self.device_manager.current_motor485,self.param_storage.set_motor_speed_post))
        self.main_window.btn_stop_motor_post.clicked.connect(lambda :Motor_485_idm42_stop_stirrer(self.device_manager.current_motor485))
        self.main_window.btn_gas_valve.clicked.connect(lambda :Valve_change_state(self.device_manager.current_gas_valve))
        self.main_window.btn_discharge_valve.clicked.connect(lambda :Valve_change_state(self.device_manager.current_discharge_valve))
        self.main_window.btn_liquid_return_valve.clicked.connect(lambda :Valve_change_state(self.device_manager.current_liquid_return_valve))
        self.main_window.btn_water_valve.clicked.connect(lambda :Valve_change_state(self.device_manager.current_water_valve))
        #反应器添加溶液部分按钮连接
        self.main_window.btn_add_solution_a.clicked.connect(
            lambda: self.set_button_color(self.main_window.btn_add_solution_a,"blue")
        )
        self.main_window.btn_add_solution_a.clicked.connect(
            lambda: Add_Solution_to_Reactor_Bond(self.device_manager,self.ui_feedback,1,self.param_storage.set_dosage_a,self.param_storage.reactor.number)
        )
        self.main_window.btn_add_solution_b.clicked.connect(
            lambda: self.set_button_color(self.main_window.btn_add_solution_b, "blue")
        )
        self.main_window.btn_add_solution_b.clicked.connect(
            lambda: Add_Solution_to_Reactor_Bond(self.device_manager,self.ui_feedback,2,self.param_storage.set_dosage_b,self.param_storage.reactor.number)
        )
        self.main_window.btn_add_solution_c.clicked.connect(
            lambda: self.set_button_color(self.main_window.btn_add_solution_c, "blue")
        )
        self.main_window.btn_add_solution_c.clicked.connect(
            lambda: Add_Solution_to_Reactor_Bond(self.device_manager,self.ui_feedback,3,self.param_storage.set_dosage_c,self.param_storage.reactor.number)
        )
        self.main_window.btn_add_solution_d.clicked.connect(
            lambda: self.set_button_color(self.main_window.btn_add_solution_d, "blue")
        )
        self.main_window.btn_add_solution_d.clicked.connect(
            lambda: Add_Solution_to_Reactor_Bond(self.device_manager,self.ui_feedback,4,self.param_storage.set_dosage_d,self.param_storage.reactor.number)
        )

        #后处理部分添加溶液按钮连接
        self.main_window.btn_inject_solution_a.clicked.connect(
            lambda: self.set_button_color(self.main_window.btn_inject_solution_a,"blue")
        )
        self.main_window.btn_inject_solution_a.clicked.connect(
            lambda: Add_reactsolution_Post(self.device_manager,self.ui_feedback,self.param_storage.set_dosage_inject_a,self.param_storage.set_post_inject_speed_a,self.param_storage.posttreatmentmodule.number)
        )
        self.main_window.btn_inject_solution_b.clicked.connect(
            lambda: self.set_button_color(self.main_window.btn_inject_solution_b, "blue")
        )
        self.main_window.btn_inject_solution_b.clicked.connect(
            lambda: Add_goodsolution_Post(self.device_manager,self.ui_feedback,self.param_storage.set_dosage_inject_b,self.param_storage.set_post_inject_speed_b,self.param_storage.posttreatmentmodule.number)
        )
        
        self.main_window.btn_inject_solution_c.clicked.connect(
            lambda: self.set_button_color(self.main_window.btn_inject_solution_c, "blue")
        )       
        self.main_window.btn_inject_solution_c.clicked.connect(
            lambda: Add_badsolution_Post(self.device_manager,self.ui_feedback,self.param_storage.set_dosage_inject_c,self.param_storage.set_post_inject_speed_c,self.param_storage.posttreatmentmodule.number)
        )
        self.main_window.btn_clean_step_a.clicked.connect(
            lambda: self.set_button_color(self.main_window.btn_clean_step_a, "blue")
        )
        self.main_window.btn_clean_step_a.clicked.connect(
            lambda: Clean_Step_A_Post(self.device_manager,self.ui_feedback,self.param_storage.set_dosage_clean_a,self.param_storage.set_post_inject_speed_clean_a,self.param_storage.posttreatmentmodule.number)
        )
        self.main_window.btn_clean_step_b.clicked.connect(
            lambda: self.set_button_color(self.main_window.btn_clean_step_b, "blue")
        )
        self.main_window.btn_clean_step_b.clicked.connect(
            lambda: Clean_Step_B_Post(self.device_manager,self.ui_feedback,self.param_storage.set_dosage_clean_b,self.param_storage.set_post_inject_speed_clean_b,self.param_storage.posttreatmentmodule.number)
        )
        #自动流程按钮绑定
        self.main_window.btn_settle_module1.clicked.connect(lambda: Auto_SettleProgram_Bond(self.device_manager,self.ui_feedback,0))
        self.main_window.btn_clean_module1.clicked.connect(lambda: Auto_CleanProgram_Bond(self.device_manager,self.ui_feedback,0))
        self.main_window.btn_settle_module2.clicked.connect(lambda: Auto_SettleProgram_Bond(self.device_manager,self.ui_feedback,1))
        self.main_window.btn_clean_module2.clicked.connect(lambda: Auto_CleanProgram_Bond(self.device_manager,self.ui_feedback,1))
        self.main_window.btn_settle_module3.clicked.connect(lambda: Auto_SettleProgram_Bond(self.device_manager,self.ui_feedback,2))
        self.main_window.btn_clean_module3.clicked.connect(lambda: Auto_CleanProgram_Bond(self.device_manager,self.ui_feedback,2))
        self.main_window.btn_settle_module4.clicked.connect(lambda: Auto_SettleProgram_Bond(self.device_manager,self.ui_feedback,3))
        self.main_window.btn_clean_module4.clicked.connect(lambda: Auto_CleanProgram_Bond(self.device_manager,self.ui_feedback,3))

        #工艺流程导入按钮绑定
        self.main_window.btn_import_process.clicked.connect(lambda: Import_Process_Bond(self.main_window.table_process))
        #工艺流程执行按钮绑定
        self.main_window.btn_execute_process.clicked.connect(lambda: Execute_Bond(self.device_manager))

        #测试按钮绑定
        # 抓取加液头按钮绑定
        self.main_window.btn_grab_a.clicked.connect(lambda: Axis_Move_In_Thread(self.device_manager, self.ui_feedback, AxisPosition.Adder_1))
        self.main_window.btn_grab_b.clicked.connect(lambda: Axis_Move_In_Thread(self.device_manager, self.ui_feedback, AxisPosition.Adder_2))
        self.main_window.btn_grab_c.clicked.connect(lambda: Axis_Move_In_Thread(self.device_manager, self.ui_feedback, AxisPosition.Adder_3))
        self.main_window.btn_grab_d.clicked.connect(lambda: Axis_Move_In_Thread(self.device_manager, self.ui_feedback, AxisPosition.Adder_4))
        self.main_window.btn_grab_e.clicked.connect(lambda: Axis_Move_In_Thread(self.device_manager, self.ui_feedback, AxisPosition.Adder_5))
        
        # 反应器点位按钮绑定
        self.main_window.btn_reactor_1.clicked.connect(lambda: Axis_Move_In_Thread(self.device_manager, self.ui_feedback, AxisPosition.Reactor_1))
        self.main_window.btn_reactor_2.clicked.connect(lambda: Axis_Move_In_Thread(self.device_manager, self.ui_feedback, AxisPosition.Reactor_2))
        self.main_window.btn_reactor_3.clicked.connect(lambda: Axis_Move_In_Thread(self.device_manager, self.ui_feedback, AxisPosition.Reactor_3))
        self.main_window.btn_reactor_4.clicked.connect(lambda: Axis_Move_In_Thread(self.device_manager, self.ui_feedback, AxisPosition.Reactor_4))
        # 待机位置点位按钮绑定
        self.main_window.btn_return_standby.clicked.connect(lambda: Axis_Move_In_Thread(self.device_manager, self.ui_feedback, AxisPosition.HOME))
        # 夹爪控制按钮绑定
        self.main_window.btn_init_claw.clicked.connect(lambda: Gripper_init_In_Thread(self.device_manager, self.ui_feedback))
        self.main_window.btn_grip_claw.clicked.connect(lambda: Gripper_on_In_Thread(self.device_manager, self.ui_feedback))
        self.main_window.btn_release_claw.clicked.connect(lambda: Gripper_off_In_Thread(self.device_manager, self.ui_feedback))
        
        # 轴控制按钮绑定
        self.main_window.btn_axis_power_on.clicked.connect(lambda: Axis_Power_on(self.device_manager))
        self.main_window.btn_axis_home.clicked.connect(lambda: Axis_Origin_In_Thread(self.device_manager, self.ui_feedback))
        self.main_window.btn_axis_reset.clicked.connect(lambda: Axis_Reset(self.device_manager))
        # 测试用泵按钮绑定
        self.main_window.btn_add_liquid.clicked.connect(lambda: FixPump_Inject_In_Thread(self.device_manager, self.ui_feedback, self.param_storage.select_test_head, self.param_storage.set_test_dosage))
        self.main_window.btn_reset_pump.clicked.connect(lambda: FixPump_reset(self.device_manager, self.param_storage.select_test_head))
        # 测试界面 多步动作按钮绑定
        self.main_window.btn_test_multi_step.clicked.connect(lambda: Test_MultiStepAction_Bond(self.device_manager, self.ui_feedback))
        
        # 反应器气阀控制按钮绑定
        self.main_window.btn_valve_open_1.clicked.connect(lambda: Reactor_N2_on(self.device_manager, 1))
        self.main_window.btn_valve_open_2.clicked.connect(lambda: Reactor_N2_on(self.device_manager, 2))
        self.main_window.btn_valve_open_3.clicked.connect(lambda: Reactor_N2_on(self.device_manager, 3))
        self.main_window.btn_valve_open_4.clicked.connect(lambda: Reactor_N2_on(self.device_manager, 4))
        
        self.main_window.btn_valve_close_1.clicked.connect(lambda: Reactor_N2_off(self.device_manager, 1))
        self.main_window.btn_valve_close_2.clicked.connect(lambda: Reactor_N2_off(self.device_manager, 2))
        self.main_window.btn_valve_close_3.clicked.connect(lambda: Reactor_N2_off(self.device_manager, 3))
        self.main_window.btn_valve_close_4.clicked.connect(lambda: Reactor_N2_off(self.device_manager, 4))
        # 为测试界面所有按钮（除了加液和复位）添加点击变蓝色的绑定
        test_buttons = [
            # 抓取加液头按钮
            self.main_window.btn_grab_a, self.main_window.btn_grab_b, 
            self.main_window.btn_grab_c, self.main_window.btn_grab_d, 
            self.main_window.btn_grab_e,
            # 反应器点位按钮
            self.main_window.btn_reactor_1, self.main_window.btn_reactor_2, 
            self.main_window.btn_reactor_3, self.main_window.btn_reactor_4,
            # 夹爪控制按钮
            self.main_window.btn_init_claw, self.main_window.btn_grip_claw, 
            self.main_window.btn_release_claw,
            # 轴控制按钮
            self.main_window.btn_axis_power_on, self.main_window.btn_axis_home, 
            self.main_window.btn_axis_reset
        ]
        
        for button in test_buttons:
            button.clicked.connect(lambda checked, btn=button: self.set_button_color(btn,"blue"))


    def refresh_serial_ports(self, combo_box:QComboBox):
        """
        扫描当前可用串口，并将其添加到传入的QComboBox控件中
        :param combo_box: QComboBox控件
        """
        combo_box.clear()
        ports = serial.tools.list_ports.comports()
        for port in ports:
            combo_box.addItem(port.device)
    
    def set_button_color(self, button: QPushButton,color:str):
        """
        设置按钮颜色，根据阀门状态或指定为蓝色
        
        Args:
            button (QPushButton): 需要设置颜色的按钮
            is_open (bool, optional): 阀门状态，True表示开启（绿色），False表示关闭（红色）
            is_blue (bool): 是否强制设置为蓝色状态
        """
        if color=="blue":
            # 蓝色状态
            button.setStyleSheet("""
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    border: 1px solid #1976D2;
                    padding: 5px;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background-color: #1976D2;
                }
                QPushButton:pressed {
                    background-color: #1565C0;
                }
            """)
        elif color=="green":
            # 开启状态：绿色
            button.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border: 1px solid #45a049;
                    padding: 5px;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
                QPushButton:pressed {
                    background-color: #3d8b40;
                }
            """)
        elif color=="red":
            # 关闭状态：红色
            button.setStyleSheet("""
                QPushButton {
                    background-color: #f44336;
                    color: white;
                    border: 1px solid #da190b;
                    padding: 5px;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background-color: #da190b;
                }
                QPushButton:pressed {
                    background-color: #ba160c;
                }
            """)

    def set_button_color_by_status(self, button, status):
        """
        根据逻辑值设置按钮颜色

        Args:
            button (QPushButton): 要设置颜色的按钮
            status (bool): 逻辑状态值，True为绿色，False为红色
        """
        if status:
            # 逻辑值为真时，设置按钮为绿色
            button.setStyleSheet("""
                QPushButton {
                    background-color: green;
                    color: white;
                    font-weight: bold;
                    border: 2px solid #2e7d32;
                    border-radius: 5px;
                    padding: 8px 16px;
                }
                QPushButton:hover {
                    background-color: #2e7d32;
                }
                QPushButton:pressed {
                    background-color: #1b5e20;
                }
            """)
        else:
            # 逻辑值为假时，设置按钮为红色
            button.setStyleSheet("""
                QPushButton {
                    background-color: red;
                    color: white;
                    font-weight: bold;
                    border: 2px solid #d32f2f;
                    border-radius: 5px;
                    padding: 8px 16px;
                }
                QPushButton:hover {
                    background-color: #d32f2f;
                }
                QPushButton:pressed {
                    background-color: #b71c1c;
                }
            """)