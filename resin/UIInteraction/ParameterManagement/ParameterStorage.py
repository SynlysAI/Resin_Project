from Common import Global

class ParameterStorage:
    class Reactor:
        def __init__(self,number):
            self.temp_sense_address = Global.TEMP_SENSE_ADDRESSES[number]
            self.motor_axis = Global.MOTOR_AXIS_ADDRESSES[number]
            self.number=number
        def set(self,number):
            self.temp_sense_address = Global.TEMP_SENSE_ADDRESSES[number]
            self.motor_axis = Global.MOTOR_AXIS_ADDRESSES[number]
            self.number = number

    class PostTreatmentModule:
        def __init__(self,number):
            self.pump_address = Global.PUMP_ADDRESS[number]
            self.valve_address = Global.SWITCH_VALVE_ADDRESS[number]
            self.motor_address = Global.MOTOR485_ADDRESS[number]
            self.gas_valve = Global.GAS_VALVES[number]
            self.discharge_valve = Global.DISCHARGE_VALVES[number]
            self.liquid_return_valve = Global.LIQUID_RETURN_VALVES[number]
            self.number=number
        def set(self,number):
            self.pump_address = Global.PUMP_ADDRESS[number]
            self.valve_address = Global.SWITCH_VALVE_ADDRESS[number]
            self.motor_address = Global.MOTOR485_ADDRESS[number]
            self.gas_valve = Global.GAS_VALVES[number]
            self.discharge_valve = Global.DISCHARGE_VALVES[number]
            self.liquid_return_valve = Global.LIQUID_RETURN_VALVES[number]
            self.number=number

    def __init__(self):
        #存储设置参数，从inputActionManager类中的输入框得到
        self.is_reactor_connected = False  # 反应器模块连接状态
        self.is_postprocessing_connected = False  # 后处理模块连接状态
        # 初始化所有可能用到的变量
        self.select_port = ''  # 反应器选择的串口
        self.select_port_fixpump = ''  # 固定泵选择的串口
        self.select_port_post = ''  # 后处理模块选择的串口
        
        self.reactor = self.Reactor(0)
        self.posttreatmentmodule=self.PostTreatmentModule(0)
        
        
        # 第一标签页：指定模块设置
        self.set_temperature = 0.0
        self.set_motor_speed = 0
        self.set_dosage_a = 0.0
        self.set_dosage_b = 0.0
        self.set_dosage_c = 0.0
        self.set_dosage_d = 0.0
        
        # 第二标签页：后处理模块设置
        self.set_dosage_inject_a = 0.0
        self.set_dosage_inject_b = 0.0
        self.set_dosage_inject_c = 0.0
        self.set_dosage_clean_a = 0.0
        self.set_dosage_clean_b = 0.0
        self.set_post_inject_speed_a = 0.0
        self.set_post_inject_speed_b = 0.0
        self.set_post_inject_speed_c = 0.0
        self.set_post_inject_speed_clean_a = 0.0
        self.set_post_inject_speed_clean_b = 0.0
        self.set_motor_speed_post = 0

               
        # 第三标签页：三轴位置标定
        # 标定位置坐标
        self.set_calib1_x = 0.0
        self.set_calib1_y = 0.0
        self.set_calib1_z = 0.0
        self.set_calib2_x = 0.0
        self.set_calib2_y = 0.0
        self.set_calib2_z = 0.0
        self.set_calib3_x = 0.0
        self.set_calib3_y = 0.0
        self.set_calib3_z = 0.0
        self.set_calib4_x = 0.0
        self.set_calib4_y = 0.0
        self.set_calib4_z = 0.0
        # 位置设定
        self.set_x_pos = 0.0
        self.set_y_pos = 0.0
        self.set_z_pos = 0.0
        self.set_x_speed = 0.0
        self.set_y_speed = 0.0
        self.set_z_speed = 0.0

        #反应器部分显示参数
        self.get_motor_state = False
        self.get_motor_speed = 0
        self.get_temprature = 0.0
        self.get_motor_state_post = False
        self.get_motor_speed_post = 0
        self.get_gas_valve_state = False
        self.get_discharge_valve_state = False
        self.get_liquid_return_valve_state = False
        self.get_water_valve_state = False
        
        # 测试界面标签页
        self.set_test_dosage = 0.0  # 加液量输入框
        self.select_test_head = 0  # 加液头选择下拉框
        # 测试选择泵、泵配套氮气阀门、配套进液阀门
        self.select_test_pump = 0  # 选择的泵索引
