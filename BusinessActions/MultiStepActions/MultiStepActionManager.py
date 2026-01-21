
from BusinessActions.DeviceManager import DeviceManager
from BusinessActions.SingleStepActions.MotorAction import Motor_485_idm42_start_stirrer, Motor_485_idm42_stop_stirrer, Motor_485_idm42_time_stir, Start_Reactor_Stirrer
from BusinessActions.SingleStepActions.ValveAction import Reactor_N2_off, Reactor_N2_on, Valve_close, Valve_open
from BusinessActions.UIFeedback.UIFeedbackHandler import UIFeedbackHandler
from Common.Global import Bottle
import time
import threading

from UIInteraction.UIGenerator.MainUI import MainUI

def Add_reactsolution(deviceManager:DeviceManager,volume:float,input_speed:float,module_number:int=1):
    Solution_transfer_Post(deviceManager,Bottle.Reaction,Bottle.Reaction,volume,input_speed,module_number=module_number)

def Add_reactsolution_Post(deviceManager:DeviceManager,uifeedback:UIFeedbackHandler,volume:float,input_speed:float,module_number:int=1):
    thread=threading.Thread(
        target=Solution_transfer_with_uichange,args=(deviceManager,uifeedback,Bottle.Reaction,Bottle.Reaction,volume,input_speed,module_number)
    )
    thread.start()

def Add_goodsolution_Post(deviceManager:DeviceManager,uifeedback:UIFeedbackHandler,volume:float,input_speed:float,module_number:int=1):
    thread = threading.Thread(
        target=Solution_transfer_with_uichange,
        args=(deviceManager, uifeedback, Bottle.GoodSolution, Bottle.TheBigBottle, volume, input_speed, module_number)
    )
    thread.start()

def Add_goodsolution(deviceManager:DeviceManager,volume:float,input_speed:float,module_number:int=1):
    Solution_transfer_Post(deviceManager,Bottle.GoodSolution,Bottle.TheBigBottle,volume,input_speed,module_number=module_number)

def Add_badsolution_Post(deviceManager:DeviceManager,uifeedback:UIFeedbackHandler,volume:float,input_speed:float,module_number:int=1):
    thread = threading.Thread(
        target=Solution_transfer_with_uichange,
        args=(deviceManager, uifeedback, Bottle.BadSolution, Bottle.TheBigBottle, volume, input_speed, module_number)
    )
    thread.start()

def Add_badsolution(deviceManager:DeviceManager,volume:float,input_speed:float,module_number:int=1):
    Solution_transfer_Post(deviceManager,Bottle.BadSolution,Bottle.TheBigBottle,volume,input_speed,module_number=module_number)

def Clean_Step_A_Post(deviceManager:DeviceManager,uifeedback:UIFeedbackHandler,volume:float,input_speed:float,module_number:int=1):
    #使用良溶剂注入需要先将良溶剂排入反应瓶
    thread = threading.Thread(
        target=Clean_Step_A_with_uichange,
        args=(deviceManager, uifeedback, volume, input_speed, module_number)
    )
    thread.start()

def Clean_Step_A(deviceManager:DeviceManager,volume:float,input_speed:float,module_number:int=1):
    Solution_transfer_Post(deviceManager,Bottle.GoodSolution,Bottle.Reaction,volume,input_speed,module_number=module_number)


def Clean_Step_A_with_uichange(deviceManager:DeviceManager,uifeedback:UIFeedbackHandler,volume:float,input_speed:float,module_number:int=1):
    uifeedback.control_ui_signal_post.emit()
    Clean_Step_A(deviceManager,volume,input_speed,module_number=module_number)
    uifeedback.reset_ui_signal_post.emit()

def Clean_Step_B_Post(deviceManager:DeviceManager,uifeedback:UIFeedbackHandler,volume:float,input_speed:float,module_number:int=1):
    #再将反应瓶内的良溶剂吸收排入沉降瓶中
    thread = threading.Thread(
        target=Solution_transfer_with_uichange,
        args=(deviceManager, uifeedback, Bottle.Reaction, Bottle.Reaction, volume, input_speed, module_number)
    )
    thread.start()

def Clean_Step_B(deviceManager:DeviceManager,volume:float,input_speed:float,module_number:int=1):
    Solution_transfer_Post(deviceManager,Bottle.Reaction,Bottle.Reaction,volume,input_speed,module_number=module_number)

def Air_push_back(deviceManager:DeviceManager,volume:float,input_speed:float,module_number:int=1):
    Solution_transfer_Post(deviceManager,Bottle.Air,Bottle.Reaction,volume,input_speed,module_number=module_number)

def Solution_transfer_Post(deviceManager:DeviceManager,origin_bottle:Bottle,end_bottle:Bottle,volume:float,input_speed,indraft_speed:float=4.0,module_number:int=1):
    """
    后处理模块溶液转移
    :param DeviceManager: 设备管理器实例
    :param volume: 转移体积，单位毫升
    :param origin_bottle: 源瓶
    :param end_bottle: 目标瓶
    :param input_speed: 注入速度，单位毫升每分钟
    :param indraft_speed: 吸入速度，单位毫升每分钟，默认值为3.0ml/s
    :param module_number: 模块编号，默认值为1
    """
    MAX_VOLUME = 25.0
    pump= deviceManager.pumps[module_number]
    switchvalve = deviceManager.switch_valves[module_number]
    water_valve = deviceManager.water_valves[module_number]
    

    
    # 对吸入的溶液量进行判断
    inputvolume = 0.0
    recycle = 1
    leftvolume = 0
    sum_volume=0.0
    if volume <= MAX_VOLUME:
        inputvolume = volume
        recycle = 1
        leftvolume = 0
    elif volume > MAX_VOLUME:
        inputvolume = MAX_VOLUME
        recycle = volume // MAX_VOLUME + 1
        leftvolume = volume % MAX_VOLUME
    # 执行液体注入
    while True:
        # 设置切换阀对准指定的溶液瓶
        time.sleep(1)

        is_pos_right = switchvalve.move_to_position(origin_bottle.value)
        while not is_pos_right:
            is_pos_right = switchvalve.move_to_position(origin_bottle.value)
        time.sleep(1)
        print("请先等待泵复位")
        pump.force_reset()
        time.sleep(1)
        pump.set_speed(indraft_speed)
        #当且仅当加反应液的时候，才去操纵水阀门
        if origin_bottle==Bottle.Reaction and end_bottle==Bottle.Reaction:
            water_valve.close()
        time.sleep(2)
        pump.move_absolute(inputvolume)
        # 设置切换阀对准后处理瓶子
        time.sleep(1)
        is_pos_right = switchvalve.move_to_position(end_bottle.value)
        while not is_pos_right:
            is_pos_right=switchvalve.move_to_position(end_bottle.value)
        # 当且仅当加反应液的时候，才去操纵水阀门
        if origin_bottle == Bottle.Reaction and end_bottle == Bottle.Reaction:
            water_valve.open()
        time.sleep(1)
        # 将溶液注入后处理瓶子
        pump.set_speed(input_speed)
        time.sleep(2)
        pump.move_absolute(0)
        sum_volume+=inputvolume
        print("当次溶液转移完成，已转移",sum_volume,"毫升")
        #关掉水阀
        water_valve.close()
        recycle -= 1
        if recycle == 0:
            break
        if recycle == 1:
            inputvolume = leftvolume
    
    #溶液转移完成后，切换阀位置复位至1号口
    is_pos_right = switchvalve.move_to_position(Bottle.Reaction.value)
    while not is_pos_right:
        is_pos_right = switchvalve.move_to_position(Bottle.Reaction.value)
    print("切换阀位置复位至1号口")

    return True

def Solution_transfer_with_uichange(deviceManager:DeviceManager,uifeedback:UIFeedbackHandler,origin_bottle:Bottle,end_bottle:Bottle,volume:float,input_speed,module_number:int=1):
    uifeedback.control_ui_signal_post.emit()
    result=Solution_transfer_Post(deviceManager,origin_bottle,end_bottle,volume,input_speed,module_number=module_number)
    uifeedback.reset_ui_signal_post.emit()
    return result

def Auto_SettleProgram(deviceManager:DeviceManager,module_number:int):
    """
    自动沉降程序
    :param DeviceManager: 设备管理器实例
    :param uifeedback: UI反馈处理器实例
    """
    #先将自动化程序中的各个参数固定下来
    looptimes=2
    Badsolution_input_volume=400#经过标定测试之后的数值
    Badsolution_input_speed=4.0
    Reactionsolution_input_volume=20
    Reactionsolution_input_speed=0.3
    Goodsolution_input_volume=3
    Goodsolution_indraft_speed=0.3
    Goodsolution_input_speed=0.3
    stirrer_speed=500
    first_stir_time=20
    second_stir_time=10
    pour_time=300#泵出时间，单位秒
    #沉降过程
    for i in range(looptimes):
        Add_badsolution(deviceManager,Badsolution_input_volume,Badsolution_input_speed,module_number)
        print("不良溶剂添加已完成，第",i+1,"轮")
        time.sleep(1)
        Motor_485_idm42_start_stirrer(deviceManager.motors485[module_number],stirrer_speed)
        print("搅拌器已启动，第",i+1,"轮")
        time.sleep(1)
        Add_reactsolution(deviceManager,Reactionsolution_input_volume,Reactionsolution_input_speed,module_number)
        Add_reactsolution(deviceManager,Reactionsolution_input_volume,Reactionsolution_input_speed,module_number)
        print("反应液添加已完成，第",i+1,"轮")
        time.sleep(1)
        #添加完反应液后，进行吸气反推，将多余反应液推回反应瓶，以免与不良溶剂混搅在管路内
        Air_push_back(deviceManager,24.5,2.0,module_number)
        print("多余反应液已推回反应瓶，第",i+1,"轮")
        # 等待搅拌时间，每秒打印已等待的时间
        for elapsed_time in range(1, first_stir_time + 1):
            time.sleep(1)
            print(f"正在搅拌，已等待 {elapsed_time} /{first_stir_time}秒，第 {i+1} 轮")
        time.sleep(1)
        Motor_485_idm42_stop_stirrer(deviceManager.motors485[module_number])
        print("开始泵出废液搅拌器速度降低，第",i+1,"轮")
        time.sleep(1)
        Valve_open(deviceManager.gas_valves[module_number])
        Valve_open(deviceManager.discharge_valves[module_number])
        print("泵出废液，第",i+1,"轮")
        # 等待泵出时间，每秒打印已等待的时间
        for elapsed_time in range(1, pour_time + 1):
            time.sleep(1)
            print(f"正在泵出废液，已等待 {elapsed_time} /{pour_time}秒，第 {i+1} 轮")
        Valve_close(deviceManager.gas_valves[module_number])
        Valve_close(deviceManager.discharge_valves[module_number])
        print("泵出完成，第",i+1,"轮")

        print("搅拌器已停止，第",i+1,"轮")
        time.sleep(1)

    for i in range(1):
        #管路回收过程
        print("开始进行管路回收,第",i+1,"轮")
        Add_badsolution(deviceManager,Badsolution_input_volume,Badsolution_input_speed,module_number)
        print("不良溶剂已经泵入，第",i+1,"轮")
        time.sleep(1)
        Motor_485_idm42_start_stirrer(deviceManager.motors485[module_number],stirrer_speed)
        print("搅拌器已启动，等待良溶剂进入，第",i+1,"轮")
        
        Clean_Step_A(deviceManager,Goodsolution_input_volume,Goodsolution_indraft_speed,module_number)
        time.sleep(1)
        print("3ml良溶剂已经泵入反应瓶，第",i+1,"轮")
        Clean_Step_B(deviceManager,Goodsolution_input_volume,Goodsolution_input_speed,module_number)
        print("3ml良溶剂已从反应瓶泵入沉降瓶，第",i+1,"轮")
        
        # 等待搅拌，
        for elapsed_time in range(1, second_stir_time + 1):
            time.sleep(1)
            print(f"管路回收过程：正在搅拌，已等待 {elapsed_time} /{second_stir_time}秒，第 {i+1} 轮")
        print("管路回收过程：搅拌完成，第",i+1,"轮")
        time.sleep(1)
        Motor_485_idm42_stop_stirrer(deviceManager.motors485[module_number])
        print("搅拌器已停止，第",i+1,"轮")
        time.sleep(1)
        Valve_open(deviceManager.gas_valves[module_number])
        Valve_open(deviceManager.discharge_valves[module_number])
        print("泵出废液，第",i+1,"轮")
        # 等待泵出时间，每秒打印已等待的时间
        for elapsed_time in range(1, pour_time + 1):
            time.sleep(1)
            print(f"正在泵出废液，已等待 {elapsed_time} /{pour_time}秒，第 {i+1} 轮")
        Valve_close(deviceManager.gas_valves[module_number])
        Valve_close(deviceManager.discharge_valves[module_number])
    print("完整沉降过程已完成，请人工拆下沉降瓶取固体")

def Auto_SettleProgram_with_uichange(deviceManager:DeviceManager,uifeedback:UIFeedbackHandler,module_number:int):
    uifeedback.auto_settle_program_signal.emit(module_number)
    Auto_SettleProgram(deviceManager,module_number)
    uifeedback.reset_auto_settle_program_signal.emit(module_number)

def Auto_SettleProgram_Bond(deviceManager:DeviceManager,uifeedback:UIFeedbackHandler,module_number:int):
    thread=threading.Thread(target=Auto_SettleProgram_with_uichange, args=(deviceManager,uifeedback,module_number))
    thread.start()

def Auto_CleanProgram(deviceManager:DeviceManager,module_number:int):
    """
    自动清洁程序
    :param DeviceManager: 设备管理器实例
    """
    #先将自动化程序中的各个参数固定下来
    looptimes=3
    Clean_solution_volume=50
    clean_solution_speed=3.0
    stirrer_speed=500
    stir_time=300
    pour_time=300#泵出时间，单位秒
    #清洁过程
    for i in range(looptimes):
        Clean_Step_A(deviceManager,Clean_solution_volume,clean_solution_speed,module_number)
        print("清洁过程：良溶剂已泵入反应瓶，第",i+1,"轮")
        time.sleep(1)
        Motor_485_idm42_start_stirrer(deviceManager.motors485[module_number],stirrer_speed)
        print("清洁过程：搅拌器已启动，第",i+1,"轮")
        time.sleep(1)
        Clean_Step_B(deviceManager,Clean_solution_volume,clean_solution_speed,module_number)
        print("清洁过程：良溶剂已从反应瓶泵入沉降瓶，第",i+1,"轮")
        time.sleep(1)
        # 等待搅拌时间，每秒打印已等待的时间
        for elapsed_time in range(1, stir_time + 1):
            time.sleep(1)
            print(f"清洁过程：正在搅拌，已等待 {elapsed_time} /{stir_time}秒，第 {i+1} 轮")
        time.sleep(1)
        Motor_485_idm42_stop_stirrer(deviceManager.motors485[module_number])
        print("清洁过程：搅拌器已停止，第",i+1,"轮")
        time.sleep(1)
        #泵出废液
        Valve_open(deviceManager.gas_valves[module_number])
        Valve_open(deviceManager.discharge_valves[module_number])
        print("清洁过程：泵出清洁液，第",i+1,"轮")
        # 等待泵出时间，每秒打印已等待的时间
        for elapsed_time in range(1, pour_time + 1):
            time.sleep(1)
            print(f"清洁过程：正在泵出清洁液，已等待 {elapsed_time} /{pour_time}秒，第 {i+1} 轮")
        Valve_close(deviceManager.gas_valves[module_number])
        Valve_close(deviceManager.discharge_valves[module_number])
        print("清洁过程：泵出完成，第",i+1,"轮")
        time.sleep(1)

def Auto_CleanProgram_with_uichange(deviceManager:DeviceManager,uifeedback:UIFeedbackHandler,module_number:int):
    uifeedback.auto_clean_program_signal.emit(module_number)
    Auto_CleanProgram(deviceManager,module_number)
    uifeedback.reset_auto_clean_program_signal.emit(module_number)

def Auto_CleanProgram_Bond(deviceManager:DeviceManager,uifeedback:UIFeedbackHandler,module_number:int):
    thread=threading.Thread(target=Auto_CleanProgram_with_uichange, args=(deviceManager,uifeedback,module_number))
    thread.start()

def FixPump_Inject(deviceManager:DeviceManager,solution_number:int,volume:float):
    """
    前处理模块加液动作
    :param DeviceManager: 设备管理器实例
    :param solution_name: 溶液名称
    :param volume: 转移体积，单位毫升
    """
    self.param_storage.is_system_busy = True
    #基础固定参数
    input_speed=100 #rpm
    volume_per_round = 0.1#每转注射量，单位ml
    #通气相关参数（正常注射后，通气将管中残留液体推出）
    gas_push_round = 150 #注射后通气转数
    gas_push_speed = 300 #注射后通气转速RPM

    #实例设置
    fixpump= deviceManager.fixpumps[solution_number-1]
    gas_valve= deviceManager.fixpump_gas_valves[solution_number-1]
    input_valve= deviceManager.fixpump_input_valves[solution_number-1]

    fixpump.reset()
    time.sleep(2)
    fixpump.set_speed_rpm(input_speed)
    print(f'给定量泵设置注射速度({input_speed} rpm)')
    time.sleep(1)
    #打开三通阀，预备推入液体
    input_valve.open()
    print('定量泵进液阀打开')
    time.sleep(10)
    print("开始执行溶液注射……")
    fixpump.set_injection_volume(volume,volume_per_round)
    time.sleep(2)
    print("注射完成，开始通气排出管内剩余液体")
    input_valve.close()
    gas_valve.open()
    print("关闭进液阀门，开启通气阀门")
    fixpump.set_speed(gas_push_speed)
    print(f"设置通气转速{gas_push_speed} rpm")
    time.sleep(1)
    fixpump.set_injection_turns(gas_push_round)
    time.sleep(1)
    fixpump.reset()
    time.sleep(2)
    print("通气完成，关闭通气阀门")
    gas_valve.close()
    self.param_storage.is_system_busy = False

def FixPump_reset(deviceManager:DeviceManager,solution_number:int):
    """
    重置前处理模块
    :param DeviceManager: 设备管理器实例
    :param solution_number: 溶液编号
    """
    fixpump= deviceManager.fixpumps[solution_number-1]
    fixpump.reset()
    time.sleep(3)
    print(f"重置定量泵{solution_number}")

def FixPump_Inject_With_UISignal(deviceManager:DeviceManager, ui_feedback:UIFeedbackHandler, solution_number:int, volume:float):
    """
    带UI信号的前处理模块加液动作
    在执行前后发送UI信号，控制测试界面的按钮和进度条状态
    
    :param deviceManager: 设备管理器实例
    :param ui_feedback: UI反馈处理器实例
    :param solution_number: 溶液编号
    :param volume: 转移体积，单位毫升
    """
    try:
        # 发送测试开始信号，禁用测试界面按钮并设置进度条为不定形式
        ui_feedback.test_start_signal.emit()
        print("发送测试开始信号，禁用测试界面按钮")
        
        # 执行定量泵加液动作
        FixPump_Inject(deviceManager, solution_number, volume)
        print(f"执行定量泵加液操作，溶液编号: {solution_number}，体积: {volume} ml")
        
        # 发送测试结束信号，激活测试界面按钮并重置进度条
        ui_feedback.test_stop_signal.emit()
        print("发送测试结束信号，激活测试界面按钮")
    except Exception as e:
        print(f"执行带UI信号的定量泵加液时发生错误: {e}")
        # 即使发生错误，也要发送测试结束信号，确保界面状态正确
        ui_feedback.test_stop_signal.emit()


def FixPump_Inject_In_Thread(deviceManager:DeviceManager, ui_feedback:UIFeedbackHandler, solution_number:int, volume:float):
    """
    在子线程中执行带UI信号的前处理模块加液动作
    
    :param deviceManager: 设备管理器实例
    :param ui_feedback: UI反馈处理器实例
    :param solution_number: 溶液编号
    :param volume: 转移体积，单位毫升
    """
    # 使用threading.Thread创建并启动线程
    thread = threading.Thread(target=FixPump_Inject_With_UISignal, args=(deviceManager, ui_feedback, solution_number, volume))
    thread.start()
    print("启动定量泵加液子线程")

from BusinessActions.SingleStepActions.AxisSingleStepAction import *
def Add_Solution_to_Reactor(deviceManager:DeviceManager,solution_number:int,volume:float,reactor:int):
    """
    前处理模块加液动作
    :param DeviceManager: 设备管理器实例
    :param solution_name: 溶液名称
    :param volume: 转移体积，单位毫升
    """
    #先确认加液模块的位置
    adder_position = None

    if solution_number == 1:
        adder_position = AxisPosition.Adder_1
    elif solution_number == 2:
        adder_position = AxisPosition.Adder_2
    elif solution_number == 3:
        adder_position = AxisPosition.Adder_3
    elif solution_number == 4:
        adder_position = AxisPosition.Adder_4
    elif solution_number == 5:
        adder_position = AxisPosition.Adder_5
    else:
        print("溶液编号错误")

    #确认反应瓶位置
    reactor_position = None
    if reactor == 1:
        reactor_position = AxisPosition.Reactor_1
    elif reactor == 2:
        reactor_position = AxisPosition.Reactor_2
    elif reactor == 3:
        reactor_position = AxisPosition.Reactor_3
    elif reactor == 4:
        reactor_position = AxisPosition.Reactor_4
    elif reactor == 5:
        reactor_position = AxisPosition.Reactor_5
    elif reactor == 6:
        reactor_position = AxisPosition.Reactor_6
    elif reactor == 7:
        reactor_position = AxisPosition.Reactor_7
    elif reactor == 8:
        reactor_position = AxisPosition.Reactor_8
    else:
        print("反应瓶编号错误")

    #抓取加液模块移动到加液位置
    Axis_Move(deviceManager,adder_position)
    time.sleep(1)
    #夹取加液模块
    Gripper_on(deviceManager)
    time.sleep(1)
    #移动加液模块到反应瓶
    Axis_Move(deviceManager,reactor_position)
    time.sleep(1)
    #执行加液
    FixPump_Inject(deviceManager,solution_number,volume)
    time.sleep(1)
    #移动加液模块到原位置
    Axis_Move(deviceManager,adder_position)
    time.sleep(1)
    #松开加液模块
    Gripper_off(deviceManager)
    time.sleep(1)
    Axis_Move(deviceManager,AxisPosition.HOME)

def Add_Solution_to_Reactor_with_uichange(deviceManager:DeviceManager,uifeedback:UIFeedbackHandler,solution_number:int,volume:float,reactor:int):
    """
    前处理模块加液动作
    :param DeviceManager: 设备管理器实例
    :param solution_name: 溶液名称
    :param volume: 转移体积，单位毫升
    """
    uifeedback.control_ui_signal.emit()
    Add_Solution_to_Reactor(deviceManager,solution_number,volume,reactor)
    uifeedback.reset_ui_signal.emit()

def Add_Solution_to_Reactor_Bond(deviceManager:DeviceManager,uifeedback:UIFeedbackHandler,solution_number:int,volume:float,reactor:int):
    thread = threading.Thread(target=Add_Solution_to_Reactor_with_uichange, args=(deviceManager, uifeedback,solution_number,volume,reactor))
    thread.start()

def Test_MultiStepAction(deviceManager:DeviceManager):
    """
    测试多步动作
    :param DeviceManager: 设备管理器实例
    """
    #移动到加液头1
    Axis_Move(deviceManager,AxisPosition.Adder_1)
    time.sleep(1)
    #夹取加液模块
    Gripper_on(deviceManager)
    time.sleep(1)
    #移动到反应瓶2
    Axis_Move(deviceManager,AxisPosition.Reactor_2)
    time.sleep(1)
    # 移动到反应瓶1
    Axis_Move(deviceManager, AxisPosition.Reactor_1)
    time.sleep(1)
    #移动到反应瓶4
    Axis_Move(deviceManager,AxisPosition.Reactor_4)
    time.sleep(1)
    # 移动到反应瓶3
    Axis_Move(deviceManager, AxisPosition.Reactor_3)
    time.sleep(1)
    #移动到加液头1
    Axis_Move(deviceManager,AxisPosition.Adder_1)
    time.sleep(1)
    #松开加液模块
    Gripper_off(deviceManager)
    time.sleep(1)
    # #通给两个反应器通入氮气
    # Reactor_N2_on(deviceManager,2)
    # Reactor_N2_on(deviceManager,4)
    # #给两个反应器启动搅拌
    # Start_Reactor_Stirrer(deviceManager,2,500)
    # Start_Reactor_Stirrer(deviceManager,4,500)
    #####################################################
    #移动到加液头2
    Axis_Move(deviceManager,AxisPosition.Adder_2)
    time.sleep(1)
    #夹取加液模块
    Gripper_on(deviceManager)
    time.sleep(1)
    #移动到反应瓶2
    Axis_Move(deviceManager,AxisPosition.Reactor_2)
    time.sleep(1)
    #移动到反应瓶1
    Axis_Move(deviceManager,AxisPosition.Reactor_1)
    time.sleep(1)
    #移动到反应瓶4
    Axis_Move(deviceManager,AxisPosition.Reactor_4)
    time.sleep(1)
    # 移动到反应瓶3
    Axis_Move(deviceManager, AxisPosition.Reactor_3)
    time.sleep(1)
    #移动到加液头2
    Axis_Move(deviceManager,AxisPosition.Adder_2)
    time.sleep(1)
    #松开加液模块
    Gripper_off(deviceManager)
    time.sleep(1)
    # #关闭氮气
    # Reactor_N2_off(deviceManager,2)
    # Reactor_N2_off(deviceManager,4)
    # #################################################
    # #移动到加液头3
    # Axis_Move(deviceManager,AxisPosition.Adder_3)
    # time.sleep(1)
    # #夹取加液模块
    # Gripper_on(deviceManager)
    # time.sleep(1)
    # #移动到反应瓶2
    # Axis_Move(deviceManager,AxisPosition.Reactor_2)
    # time.sleep(1)
    # # 移动到反应瓶1
    # Axis_Move(deviceManager, AxisPosition.Reactor_1)
    # time.sleep(1)
    # #移动到反应瓶4
    # Axis_Move(deviceManager,AxisPosition.Reactor_4)
    # time.sleep(1)
    # #移动到加液头3
    # Axis_Move(deviceManager,AxisPosition.Adder_3)
    # time.sleep(1)
    # #松开加液模块
    # Gripper_off(deviceManager)
    # time.sleep(1)
    # ###########################################
    # #移动到加液头4
    # Axis_Move(deviceManager,AxisPosition.Adder_4)
    # time.sleep(1)
    # #夹取加液模块
    # Gripper_on(deviceManager)
    # time.sleep(1)
    # #移动到反应瓶2
    # Axis_Move(deviceManager,AxisPosition.Reactor_2)
    # time.sleep(1)
    # # 移动到反应瓶1
    # Axis_Move(deviceManager, AxisPosition.Reactor_1)
    # time.sleep(1)
    # #移动到反应瓶4
    # Axis_Move(deviceManager,AxisPosition.Reactor_4)
    # time.sleep(1)
    # #移动到加液头4
    # Axis_Move(deviceManager,AxisPosition.Adder_4)
    # time.sleep(1)
    # #松开加液模块
    # Gripper_off(deviceManager)
    # time.sleep(1)
    # #######################
    # #移动到加液头5
    # Axis_Move(deviceManager,AxisPosition.Adder_5)
    # time.sleep(1)
    # #夹取加液模块
    # Gripper_on(deviceManager)
    # time.sleep(1)
    # #移动到反应瓶2
    # Axis_Move(deviceManager,AxisPosition.Reactor_2)
    # time.sleep(1)
    # # 移动到反应瓶1
    # Axis_Move(deviceManager, AxisPosition.Reactor_1)
    # time.sleep(1)
    # #移动到反应瓶4
    # Axis_Move(deviceManager,AxisPosition.Reactor_4)
    # time.sleep(1)
    # #移动到加液头5
    # Axis_Move(deviceManager,AxisPosition.Adder_5)
    # time.sleep(1)
    # #松开加液模块
    # Gripper_off(deviceManager)
    # time.sleep(1)
    # #######################

    #移动到原点
    Axis_Move(deviceManager,AxisPosition.HOME)


def Test_MultiStepAction_with_uichange(deviceManager:DeviceManager,uifeedback:UIFeedbackHandler):
    """
    带UI变化的测试多步动作
    :param deviceManager: 设备管理器实例
    :param uifeedback: UI反馈处理器实例
    """
    try:
        # 发送测试开始信号，禁用测试界面按钮并设置进度条
        uifeedback.test_start_signal.emit()
        print("发送测试开始信号，禁用测试界面按钮")
        
        # 执行测试多步动作
        Test_MultiStepAction(deviceManager)
        print("执行测试多步动作")
        
        # 发送测试结束信号，激活测试界面按钮并重置进度条
        uifeedback.test_stop_signal.emit()
        print("发送测试结束信号，激活测试界面按钮")
    except Exception as e:
        print(f"执行带UI信号的测试多步动作时发生错误: {e}")
        # 即使发生错误，也要发送测试结束信号，确保界面状态正确
        uifeedback.test_stop_signal.emit()


def Test_MultiStepAction_Bond(deviceManager:DeviceManager,uifeedback:UIFeedbackHandler):
    """
    在子线程中执行带UI信号的测试多步动作
    :param deviceManager: 设备管理器实例
    :param uifeedback: UI反馈处理器实例
    """
    # 使用threading.Thread创建并启动线程
    thread = threading.Thread(target=Test_MultiStepAction_with_uichange, args=(deviceManager, uifeedback))
    thread.start()
    print("启动测试多步动作子线程")
