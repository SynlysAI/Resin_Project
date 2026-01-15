1. 创建一个直接实例化ResinWorkstation并测试所有方法的Python脚本
2. 创建一个UDP服务器用于接收和响应ResinWorkstation的命令
3. 服务器需要保存所有测试数据

**文件1: test\_resin\_workstation\_direct.py**

* 直接实例化ResinWorkstation对象

* 测试所有方法，包括连接、各种操作指令、状态查询等

* 输出测试结果

**文件2: test\_udp\_server.py**

* 创建一个UDP服务器，监听指定端口

* 接收ResinWorkstation发送的命令

* 返回模拟响应

* 将所有接收的命令和发送的响应保存到日志文件

* 支持实时查看测试数据

**实现细节**:

* UDP服务器将使用socket库实现

* 测试数据将保存为JSON格式，方便查看和分析

* 直接测试脚本将包含清晰的测试流程和结果输出

