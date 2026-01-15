import json
import socket
import threading
import time
import unittest
import os
import sys
from unittest.mock import MagicMock, patch
# 将包含unilabos的目录添加到Python路径
unilab_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../'))
sys.path.insert(0, unilab_dir)

# 然后修改导入语句
from unilabos.devices.workstation.resin_workstation.resin_workstation import ResinWorkstation, UDPClient

class TestResinWorkstation(unittest.TestCase):
    """
    ResinWorkstation 类的测试用例
    """
    
    def setUp(self):
        """
        设置测试环境
        """
        self.address = "127.0.0.1"
        self.port = 9999
        
        # 创建 ResinWorkstation 实例
        self.workstation = ResinWorkstation(
            address=self.address,
            port=self.port,
            debug_mode=False
        )
    
    def tearDown(self):
        """
        清理测试环境
        """
        if self.workstation.connected:
            self.workstation.disconnect_device()
    
    def test_init(self):
        """
        测试初始化
        """
        self.assertEqual(self.workstation.udp_client.address, self.address)
        self.assertEqual(self.workstation.udp_client.port, self.port)
        self.assertFalse(self.workstation.connected)
        self.assertEqual(self.workstation.operation_mode, "local")
    
    def test_post_init(self):
        """
        测试 post_init 方法
        """
        # 创建模拟 ROS 节点
        mock_ros_node = MagicMock()
        mock_ros_node.update_resource = MagicMock()
        
        # 调用 post_init
        self.workstation.post_init(mock_ros_node)
        
        # 验证 _ros_node 属性已设置
        self.assertEqual(self.workstation._ros_node, mock_ros_node)
    
    def test_connect_device(self):
        """
        测试连接设备
        """
        result = self.workstation.connect_device()
        self.assertTrue(result)
        self.assertTrue(self.workstation.connected)
    
    def test_disconnect_device(self):
        """
        测试断开设备连接
        """
        self.workstation.connect_device()
        result = self.workstation.disconnect_device()
        self.assertTrue(result)
        self.assertFalse(self.workstation.connected)
    
    def test_connect_with_custom_address_port(self):
        """
        测试使用自定义地址和端口连接
        """
        custom_address = "192.168.1.1"
        custom_port = 8888
        
        result = self.workstation.connect_device(custom_address, custom_port)
        self.assertTrue(result)
        self.assertEqual(self.workstation.udp_client.address, custom_address)
        self.assertEqual(self.workstation.udp_client.port, custom_port)
    
    def test_toggle_local_remote_control(self):
        """
        测试切换本地/远程控制模式
        """
        self.workstation.connect_device()
        
        # 切换到远程模式
        result = self.workstation.toggle_local_remote_control("remote")
        self.assertTrue(result)
        self.assertEqual(self.workstation.operation_mode, "remote")
        
        # 切换回本地模式
        result = self.workstation.toggle_local_remote_control("local")
        self.assertTrue(result)
        self.assertEqual(self.workstation.operation_mode, "local")
    
    def test_toggle_local_remote_control_invalid_mode(self):
        """
        测试使用无效模式切换本地/远程控制
        """
        result = self.workstation.toggle_local_remote_control("invalid_mode")
        self.assertFalse(result)
        self.assertEqual(self.workstation.operation_mode, "local")  # 模式应保持不变
    
    def test_device_status(self):
        """
        测试设备状态查询
        """
        # 未连接状态
        status = self.workstation.device_status
        self.assertEqual(status["status"], "disconnected")
        self.assertEqual(status["operation_mode"], "local")
        
        # 连接状态
        self.workstation.connect_device()
        status = self.workstation.device_status
        self.assertEqual(status["status"], "connected")
        self.assertEqual(status["operation_mode"], "local")
    
    def test_debug_mode(self):
        """
        测试调试模式
        """
        # 创建调试模式实例
        debug_workstation = ResinWorkstation(
            address=self.address,
            port=self.port,
            debug_mode=True
        )
        
        # 检查调试模式下的设备状态
        status = debug_workstation.device_status
        self.assertEqual(status["status"], "debug")
        self.assertTrue(status["connected"])
    
    def test_reactor_solution_add(self):
        """
        测试 REACTOR_SOLUTION_ADD 指令
        """
        self.workstation.connect_device()
        result = self.workstation.reactor_solution_add(
            solution_id=1,
            volume=10.0,
            reactor_id=1
        )
        self.assertTrue(result)
    
    def test_post_process_solution_add(self):
        """
        测试 POST_PROCESS_SOLUTION_ADD 指令
        """
        self.workstation.connect_device()
        result = self.workstation.post_process_solution_add(
            start_bottle="bottle1",
            end_bottle="bottle2",
            volume=5.0,
            inject_speed=2.0,
            suck_speed=3.0
        )
        self.assertTrue(result)
    
    def test_post_process_clean(self):
        """
        测试 POST_PROCESS_CLEAN 指令
        """
        self.workstation.connect_device()
        result = self.workstation.post_process_clean(post_process_id=1)
        self.assertTrue(result)
    
    def test_reactor_n2_on(self):
        """
        测试 REACTOR_N2_ON 指令
        """
        self.workstation.connect_device()
        result = self.workstation.reactor_n2_on(reactor_id=1)
        self.assertTrue(result)
    
    def test_reactor_n2_off(self):
        """
        测试 REACTOR_N2_OFF 指令
        """
        self.workstation.connect_device()
        result = self.workstation.reactor_n2_off(reactor_id=1)
        self.assertTrue(result)
    
    def test_reactor_air_on(self):
        """
        测试 REACTOR_AIR_ON 指令
        """
        self.workstation.connect_device()
        result = self.workstation.reactor_air_on(reactor_id=1)
        self.assertTrue(result)
    
    def test_reactor_air_off(self):
        """
        测试 REACTOR_AIR_OFF 指令
        """
        self.workstation.connect_device()
        result = self.workstation.reactor_air_off(reactor_id=1)
        self.assertTrue(result)
    
    def test_temp_set(self):
        """
        测试 TEMP_SET 指令
        """
        self.workstation.connect_device()
        result = self.workstation.temp_set(reactor_id=1, temperature=25.0)
        self.assertTrue(result)
    
    def test_start_reactor_stirrer(self):
        """
        测试 START_STIR 指令
        """
        self.workstation.connect_device()
        result = self.workstation.start_reactor_stirrer(reactor_id=1, speed=100.0)
        self.assertTrue(result)
    
    def test_stop_reactor_stirrer(self):
        """
        测试 STOP_STIR 指令
        """
        self.workstation.connect_device()
        result = self.workstation.stop_reactor_stirrer(reactor_id=1)
        self.assertTrue(result)
    
    def test_post_process_discharge_on(self):
        """
        测试 POST_PROCESS_DISCHARGE_ON 指令
        """
        self.workstation.connect_device()
        result = self.workstation.post_process_discharge_on(post_process_id=1)
        self.assertTrue(result)
    
    def test_post_process_discharge_off(self):
        """
        测试 POST_PROCESS_DISCHARGE_OFF 指令
        """
        self.workstation.connect_device()
        result = self.workstation.post_process_discharge_off(post_process_id=1)
        self.assertTrue(result)
    
    def test_wait(self):
        """
        测试 WAIT 指令
        """
        start_time = time.time()
        result = self.workstation.wait(seconds=1)
        end_time = time.time()
        self.assertTrue(result)
        # 验证等待时间
        self.assertAlmostEqual(end_time - start_time, 1.0, delta=0.1)
    
    def test_command_without_connection(self):
        """
        测试未连接时发送命令
        """
        result = self.workstation.reactor_solution_add(
            solution_id=1,
            volume=10.0,
            reactor_id=1
        )
        self.assertFalse(result)
    
    @patch('resin_workstation.UDPClient.send_command')
    def test_command_failure(self, mock_send_command):
        """
        测试命令执行失败的情况
        """
        # 模拟命令执行失败
        mock_send_command.return_value = {"status": "error", "message": "Test error"}
        self.workstation.connect_device()
        
        result = self.workstation.reactor_solution_add(
            solution_id=1,
            volume=10.0,
            reactor_id=1
        )
        self.assertFalse(result)
    
    def test_debug_mode_commands(self):
        """
        测试调试模式下的命令执行
        """
        # 创建调试模式实例
        debug_workstation = ResinWorkstation(
            address=self.address,
            port=self.port,
            debug_mode=True
        )
        
        # 调试模式下不需要连接设备
        result = debug_workstation.reactor_solution_add(
            solution_id=1,
            volume=10.0,
            reactor_id=1
        )
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()