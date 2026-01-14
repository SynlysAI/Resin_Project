# 项目快速入门文档

## 1. 项目概述

本项目是一个自动化控制软件系统，用于控制和监控化学反应器及其后处理模块的运行。系统通过PySide6构建图形用户界面，使用Modbus TCP和串口通信与各类设备（如电机、温度传感器、阀门、泵等）进行交互，实现自动化控制流程。

## 2. 目录结构

```
e:\PJ_Project_Software\
├── main.py                 # 程序入口文件
├── UIInteraction/          # UI交互相关模块
│   ├── UIGenerator/        # UI生成相关
│   │   └── MainUI.py       # 主界面定义
│   ├── ControlActions/     # 控制动作相关
│   │   ├── ButtonActionManager.py  # 按钮事件管理
│   │   └── InputActionManager.py   # 输入管理
│   ├── ParameterManagement/# 参数管理
│   │   └── ParameterStorage.py     # 参数存储
│   └── RealTimeUpdate/     # 实时更新
│       └── RealTimeUpdate.py       # 实时参数更新
├── BusinessActions/        # 业务动作相关
│   ├── DeviceManager.py    # 设备管理
│   ├── UIFeedback/         # UI反馈
│   │   └── UIFeedbackHandler.py    # UI反馈处理
│   ├── SingleStepActions/  # 单步动作
│   └── MultiStepActions/   # 多步动作
└── Drivers/                # 驱动程序
    └── EthernetDevices/    # 以太网设备驱动
        └── inovance_three_axis/    # 汇川三轴控制系统
```

## 3. 主要文件功能说明

### 3.1 程序入口文件 - main.py

**功能**: 程序的主入口点，负责初始化应用程序、创建核心组件实例并启动主循环。

**主要函数/类**:
- `__main__` 代码块：初始化QApplication，创建并显示MainUI窗口，启动应用程序主循环
- 核心组件实例化：MainUI、DeviceManager、InputActionManager、ButtonActionManager等

### 3.2 主界面文件 - MainUI.py

**功能**: 定义应用程序的主用户界面，包括多个标签页（指定模块设置、后处理模块设置、三轴位置标定、测试界面等）。

**主要函数/类**:
- `MainUI` 类：主窗口类，继承自QMainWindow
- `__init__` 方法：初始化界面组件和变量
- `init_ui` 方法：初始化UI布局，创建标签页和各个控件

### 3.3 设备管理文件 - DeviceManager.py

**功能**: 管理所有设备的连接、通信和控制，是系统与硬件设备交互的核心模块。

**主要函数/类**:
- `DeviceManager` 类：设备管理核心类
- `__init__` 方法：初始化设备管理器，创建参数存储和监控线程
- 连接相关方法：
  - `connect_zmc`: 连接正运动控制卡
  - `connect_serial_port`: 连接反应器串口
  - `connect_serial_port_post`: 连接后处理模块串口
  - `connect_io_control`: 连接IO控制器
  - `connect_all_reactor_devices`: 连接所有反应器设备
  - `connect_all_post_devices`: 连接所有后处理模块设备
- 断开连接相关方法：
  - `disconnect_all_reactor_devices`: 断开所有反应器设备连接
  - `disconnect_all_post_devices`: 断开所有后处理模块设备连接

### 3.4 参数存储文件 - ParameterStorage.py

**功能**: 集中管理和存储系统中的各类参数，提供参数的读写接口。

**主要函数/类**:
- `ParameterStorage` 类：参数存储核心类
- 内部子类：
  - `Reactor` 类：管理反应器模块参数
  - `PostTreatmentModule` 类：管理后处理模块参数
- 参数变量：包含反应器连接状态、串口选择、温度/速度设置值、三轴标定坐标等各类系统参数

### 3.5 UI反馈处理文件 - UIFeedbackHandler.py

**功能**: 处理UI控制信号，管理UI元素的状态更新和反馈。

**主要函数/类**:
- `UIFeedbackHandler` 类：UI反馈处理核心类，继承自QObject
- 信号定义：控制UI的各种信号（control_ui_signal、reset_ui_signal等）
- `control_ui_action` 方法：控制QT界面控件（修改背景色、禁用按钮等）
- UI元素列表：管理进度条、沉降按钮和清洁按钮等UI元素

### 3.6 按钮动作管理文件 - ButtonActionManager.py

**功能**: 管理和处理所有按钮的事件，将用户界面操作映射到相应的业务动作。

**主要函数/类**:
- `ButtonActionManager` 类：按钮控件管理器类
- `__init__` 方法：初始化按钮管理器，设置按钮连接
- `setup_button_connections` 方法：设置所有按钮的信号槽连接
- 设备控制相关连接：连接/断开、电机启动/停止、温度设置、阀门控制等
- 溶液处理相关连接：溶液注入、清洗步骤等

### 3.7 输入动作管理文件 - InputActionManager.py

**功能**: 管理UI输入框和下拉框，设置验证器并处理输入值的更新。

**主要函数/类**:
- `InputActionManager` 类：输入动作管理核心类
- `UpdateThread` 内部类：用于更新输入变量的线程
- `set_input_validators` 方法：为所有输入框设置验证器
- `get_all_input_boxes` 方法：获取所有输入框组件
- `get_all_combo_boxes` 方法：获取所有下拉框组件
- `setup_combo_box_connections` 方法：设置下拉框的信号槽连接
- `update_input_values` 方法：更新输入值到参数管理类

### 3.8 实时更新文件 - RealTimeUpdate.py

**功能**: 定期获取设备状态和参数，实现UI的实时更新。

**主要函数/类**:
- `RealTimeUpdate` 类：实时更新核心类
- `start` 方法：启动更新线程
- `stop` 方法：停止更新线程
- `_update_loop` 方法：线程主循环，定期执行更新
- `update` 方法：执行特定函数获取设备状态并更新参数

### 3.9 三轴控制系统文件 - inovance_three_axis.py

**功能**: 控制汇川三轴运动系统，实现三轴定位和运动控制。

**主要函数/类**:
- `Inovance_Three_Axis` 类：汇川三轴控制核心类
- `__init__` 方法：初始化Modbus TCP连接、加载节点配置
- 轴控制命令方法：
  - `axis_x_power_on_cmd`/`axis_x_origin_cmd`/`axis_x_stop_cmd`：X轴控制
  - `axis_y_power_on_cmd`/`axis_y_origin_cmd`/`axis_y_stop_cmd`：Y轴控制
  - `axis_z_power_on_cmd`/`axis_z_origin_cmd`/`axis_z_stop_cmd`：Z轴控制
- 功能方法：
  - `func_pack_z_home`：Z轴回原点
  - `func_pack_three_axis_move_target`：三轴移动到目标位置
  - `func_pack_standard_robot_move_cycle`：标准机器人运动循环

## 4. 核心功能模块

### 4.1 设备通信模块

**功能**: 负责与各类硬件设备进行通信，包括串口通信和Modbus TCP通信。

**主要组件**:
- 串口通信：通过`Common_Serial`类实现与串口设备的通信
- Modbus TCP通信：通过pymodbus库实现与支持Modbus TCP协议的设备通信
- 设备实例：电机、温度传感器、阀门、泵等各类设备的实例管理

### 4.2 UI交互模块

**功能**: 提供用户界面，处理用户输入并显示系统状态。

**主要组件**:
- 标签页系统：包含反应器设置、后处理设置、三轴标定和测试界面
- 控件管理：按钮、输入框、下拉框等UI控件的创建和事件处理
- 实时更新：定期刷新UI显示的设备状态和参数

### 4.3 运动控制模块

**功能**: 控制三轴运动系统和各类电机，实现精确定位和运动控制。

**主要组件**:
- 三轴控制系统：通过`Inovance_Three_Axis`类控制三轴运动
- 电机控制：包括搅拌电机、底部电机等的启动、停止和速度控制
- 运动规划：通过JSON文件定义动作序列，实现复杂的运动流程

### 4.4 参数管理模块

**功能**: 集中管理系统中的所有参数，提供统一的参数访问接口。

**主要组件**:
- 参数存储：通过`ParameterStorage`类存储和管理各类参数
- 参数映射：设备地址和参数的映射关系
- 实时监控：通过`ParameterMonitorThread`监控参数变化

## 5. 工作流程

### 5.1 系统启动流程

1. 启动应用程序（执行main.py）
2. 初始化MainUI，创建用户界面
3. 初始化DeviceManager，建立设备连接
4. 初始化InputActionManager和ButtonActionManager，设置UI交互
5. 启动RealTimeUpdate，开始实时更新UI

### 5.2 设备连接流程

1. 用户在UI中选择串口和模块
2. 点击连接按钮，触发`connnect_reactor_moudle`或`connect_post_module`
3. 系统建立串口连接和设备实例
4. 设置连接状态标志，开始监控设备参数

### 5.3 运动控制流程

1. 用户在UI中设置目标位置和速度
2. 系统通过Modbus TCP向PLC发送指令
3. PLC控制电机运动到目标位置
4. 系统实时获取运动状态并更新UI

## 6. 快速入门指南

### 6.1 环境要求

- Python 3.x
- PySide6
- pymodbus
- serial (pyserial)

### 6.2 启动系统

1. 确保所有硬件设备已连接并上电
2. 运行`python main.py`启动应用程序
3. 在主界面选择相应的串口和模块
4. 点击连接按钮建立设备连接

### 6.3 基本操作

#### 反应器控制
- 在"指定模块设置"标签页设置温度和电机速度
- 点击启动/停止按钮控制电机运行
- 点击温度设置按钮设置目标温度

#### 后处理模块控制
- 在"后处理模块设置"标签页设置各参数
- 控制阀门开关和泵的运行
- 执行溶液注入和清洗步骤

#### 三轴控制
- 在"三轴位置标定"标签页进行位置标定
- 设置目标位置和速度
- 执行三轴运动控制

### 6.4 测试界面
- 在"测试界面"标签页可以进行各种功能测试
- 包含运动控制按钮和输入文本框

## 7. 故障排除

### 7.1 连接问题
- 检查串口连接和设备电源
- 确认所选串口正确且未被其他程序占用
- 检查设备地址设置是否正确

### 7.2 通信错误
- 检查通信协议和参数设置
- 确认设备处于正常工作状态
- 尝试重启设备和应用程序

### 7.3 运动控制问题
- 检查电机和驱动器连接
- 确认运动范围设置正确
- 检查限位开关状态

---
# 新增功能说明
## 8 新增功能
### 8.1 新增UI界面
- 如果需要新增UI功能界面，需要在MainUI.py中添加新的标签页和控件。
### 8.2 新增输入文本框
- 如果需要新增输入文本框，需要在MainUI.py中添加新的QLineEdit控件。
- 需要在ParameterStorage.py中添加新的变量，用于存储文本框中的输入值。
- 需要在InputActionManager.py中的get_all_input_boxes函数中添加新文本框的名称
- 需要在InputActionManager.py中的set_input_validators函数中确认该文本框的输入验证规则。
- 需要在InputActionManager.py中的update_input_values函数中添加新文本框的更新逻辑，令变量与输入值对应。
- 完成上述设置后，可以从ParameterStorage.py中的变量获取新文本框的输入值进行使用。
### 8.3 新增按钮
- 如果需要新增按钮，需要在MainUI.py中添加新的QPushButton控件。
- 需要在ButtonActionManager.py中添加新按钮的事件处理函数。
- 完成上述设置后，点击新按钮即可触发对应的事件处理函数。
### 8.4 新增下拉框
- 如果需要新增下拉框，需要在MainUI.py中添加新的QComboBox控件。
- 需要在ParameterStorage.py中添加新的变量，用于存储下拉框中的选择值。
- 需要在InputActionManager.py中的get_all_combo_boxes函数中添加新下拉框的名称
- 需要在InputActionManager.py中的on_combo_box_changed函数中添加新下拉框的选择值更新逻辑，令变量与选择值对应。
- 完成上述设置后，可以从ParameterStorage.py中的变量获取新下拉框的选择值进行使用。
### 8.5 新增设备连接
- 如果需要新增设备连接，需要在DeviceManager.py中添加新的连接变量
- 如果需要新增控制设备，需要在DeviceManager.py中添加新的设备变量，以及在连接函数中令设备变量进行实例化



以上是本项目的快速入门文档，详细说明了项目结构、主要文件功能和工作流程。如有其他问题，请参考项目源代码或联系技术支持。"# PJ_Project_Software" 
