# 实现Resin Workstation驱动

## 1. 项目结构创建

* 创建 `c:\Users\dell\Desktop\Resin_Project\unilab\unilabos\devices\workstation\resin_workstation` 目录

* 在该目录下创建 `resin_workstation.py` 文件

## 2. 核心实现

### 2.1 UDP客户端实现

* 实现一个UDP客户端类，支持发送命令和接收响应

* 支持连接、断开连接功能

* 支持超时处理和错误重试

### 2.2 ResinWorkstation类

* 继承自 `WorkstationBase` 类

* 实现 `__init__` 方法，初始化UDP客户端

* 实现 `post_init` 方法，设置ROS节点

### 2.3 指令集实现

根据Excel指令集实现以下指令：

#### 移液操作指令集

* `REACTOR_SOLUTION_ADD` - 向反应器添加溶液

  * 参数：溶液编号（int）、加入体积（float）、反应器编号（int）

* `POST_PROCESS_SOLUTION_ADD` - 后处理溶液转移

  * 参数：出发瓶（enum）、终点瓶（enum）、加入体积（float）、注入速度（float）、吸入速度（float，默认4.0）

* `POST_PROCESS_CLEAN` - 自动清洗程序

  * 参数：后处理编号（int）

#### 反应器操作指令集

* `REACTOR_N2_ON` - 打开反应器氮气

  * 参数：反应器编号（int）

* `REACTOR_N2_OFF` - 关闭反应器氮气

  * 参数：反应器编号（int）

* `REACTOR_AIR_ON` - 打开反应器空气

  * 参数：反应器编号（int）

* `REACTOR_AIR_OFF` - 关闭反应器空气

  * 参数：反应器编号（int）

* `TEMP_SET` - 设置温度

  * 参数：反应器编号（int）、温度（float）

#### 搅拌器操作指令集

* `START_STIR` - 启动反应器搅拌器

  * 参数：反应器编号（int）、转速（float）

* `STOP_STIR` - 停止反应器搅拌器

  * 参数：反应器编号（int）

#### 后处理排液操作指令集

* `POST_PROCESS_DISCHARGE_ON` - 打开后处理排液

  * 参数：后处理编号（int）

* `POST_PROCESS_DISCHARGE_OFF` - 关闭后处理排液

  * 参数：后处理编号（int）

#### 其他指令

* `WAIT` - 等待指定时间

  * 参数：等待时间（秒，int）

### 2.4 额外指令实现

* `DEVICE_CONNECT` - 连接设备

  * 参数：IP地址（str）、端口（int）

* `DEVICE_DISCONNECT` - 断开设备连接

  * 参数：无

* `TOGGLE_LOCAL_REMOTE_CONTROL` - 切换本地/远程控制

  * 参数：控制模式（str，"local"或"remote"）

## 3. 通信协议

* 命令格式：JSON格式，包含指令名称和参数

  * 示例：`{"command": "REACTOR_SOLUTION_ADD", "params": {"solution_id": 1, "volume": 10.0, "reactor_id": 1}}`

* 响应格式：JSON格式，包含状态码和结果

  * 示例：`{"status": "success", "result": null}` 或 `{"status": "error", "message": "错误信息"}`

* 支持超时重传机制

## 4. 调试模式

* 实现调试模式，支持离线测试

* 提供模拟数据返回

## 5. 错误处理

* 实现全面的错误处理机制

* 记录详细的日志信息

* 提供友好的错误提示

## 6. 代码风格

* 遵循现有的代码风格

* 保持与coin\_cell\_assembly.py类似的结构

* 添加必要的注释和文档字符串

