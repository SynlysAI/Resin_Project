import json
import time
import os
import sys

# 将包含unilabos的目录添加到Python路径
unilab_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../'))
sys.path.insert(0, unilab_dir)

# 导入ResinWorkstation
from unilabos.devices.workstation.resin_workstation.resin_workstation import ResinWorkstation


def print_test_result(test_name, result):
    """
    打印测试结果
    
    Args:
        test_name: 测试名称
        result: 测试结果
    """
    status = "✓ PASS" if result else "✗ FAIL"
    print(f"{test_name:<50} {status}")
    return result


def main():
    """
    主测试函数
    """
    print("=" * 70)
    print("ResinWorkstation 直接测试脚本")
    print("=" * 70)
    
    # 测试配置
    address = "127.0.0.1"
    port = 9997
    
    # 创建ResinWorkstation实例
    print("\n1. 初始化测试...")
    workstation = ResinWorkstation(
        address=address,
        port=port,
        debug_mode=True
    )
    
    test_results = []
    
    # 测试初始化
    test_results.append(print_test_result("初始化ResinWorkstation", True))
    test_results.append(print_test_result("检查初始连接状态", not workstation.connected))
    test_results.append(print_test_result("检查初始操作模式", workstation.operation_mode == "local"))
    
    # 测试连接设备
    print("\n2. 连接设备测试...")
    connect_result = workstation.connect_device()
    test_results.append(print_test_result("连接设备", connect_result))
    if connect_result:
        test_results.append(print_test_result("检查连接状态", workstation.connected))
    
    # 测试设备状态查询
    print("\n3. 设备状态测试...")
    status = workstation.device_status
    test_results.append(print_test_result("获取设备状态", status is not None))
    if status:
        print(f"   设备状态: {status['status']}")
        print(f"   连接状态: {status['connected']}")
        print(f"   操作模式: {status['operation_mode']}")
    
    # 测试切换本地/远程控制模式
    print("\n4. 控制模式切换测试...")
    if workstation.connected:
        remote_result = workstation.toggle_local_remote_control("remote")
        test_results.append(print_test_result("切换到远程模式", remote_result))
        if remote_result:
            test_results.append(print_test_result("检查远程模式", workstation.operation_mode == "remote"))
        
        # 切换回本地模式
        local_result = workstation.toggle_local_remote_control("local")
        test_results.append(print_test_result("切换回本地模式", local_result))
        if local_result:
            test_results.append(print_test_result("检查本地模式", workstation.operation_mode == "local"))
    
    # 测试反应器溶液添加
    print("\n5. 反应器操作测试...")
    if workstation.connected:
        solution_add_result = workstation.reactor_solution_add(
            solution_id=1,
            volume=10.0,
            reactor_id=1
        )
        test_results.append(print_test_result("反应器添加溶液", solution_add_result))
    
    # 测试氮气控制
    if workstation.connected:
        n2_on_result = workstation.reactor_n2_on(reactor_id=1)
        test_results.append(print_test_result("打开氮气", n2_on_result))
        
        n2_off_result = workstation.reactor_n2_off(reactor_id=1)
        test_results.append(print_test_result("关闭氮气", n2_off_result))
    
    # 测试空气控制
    if workstation.connected:
        air_on_result = workstation.reactor_air_on(reactor_id=1)
        test_results.append(print_test_result("打开空气", air_on_result))
        
        air_off_result = workstation.reactor_air_off(reactor_id=1)
        test_results.append(print_test_result("关闭空气", air_off_result))
    
    # 测试温度设置
    if workstation.connected:
        temp_set_result = workstation.temp_set(reactor_id=1, temperature=25.0)
        test_results.append(print_test_result("设置温度", temp_set_result))
    
    # 测试搅拌器控制
    if workstation.connected:
        start_stir_result = workstation.start_reactor_stirrer(reactor_id=1, speed=100.0)
        test_results.append(print_test_result("启动搅拌器", start_stir_result))
        
        stop_stir_result = workstation.stop_reactor_stirrer(reactor_id=1)
        test_results.append(print_test_result("停止搅拌器", stop_stir_result))
    
    # 测试后处理系统
    print("\n6. 后处理系统测试...")
    if workstation.connected:
        # 后处理溶液转移
        transfer_result = workstation.post_process_solution_add(
            start_bottle="bottle1",
            end_bottle="bottle2",
            volume=5.0,
            inject_speed=2.0,
            suck_speed=3.0
        )
        test_results.append(print_test_result("后处理溶液转移", transfer_result))
        
        # 后处理清洗
        clean_result = workstation.post_process_clean(post_process_id=1)
        test_results.append(print_test_result("后处理清洗", clean_result))
        
        # 后处理排液控制
        discharge_on_result = workstation.post_process_discharge_on(post_process_id=1)
        test_results.append(print_test_result("打开后处理排液", discharge_on_result))
        
        discharge_off_result = workstation.post_process_discharge_off(post_process_id=1)
        test_results.append(print_test_result("关闭后处理排液", discharge_off_result))
    
    # 测试等待功能
    print("\n7. 等待功能测试...")
    start_time = time.time()
    wait_result = workstation.wait(seconds=1)
    end_time = time.time()
    wait_passed = wait_result and (end_time - start_time >= 0.9)
    test_results.append(print_test_result("等待1秒", wait_passed))
    
    # 测试调试模式
    print("\n8. 调试模式测试...")
    debug_workstation = ResinWorkstation(
        address=address,
        port=port,
        debug_mode=True
    )
    test_results.append(print_test_result("创建调试模式实例", True))
    
    # 调试模式下测试命令执行
    debug_solution_result = debug_workstation.reactor_solution_add(
        solution_id=1,
        volume=10.0,
        reactor_id=1
    )
    test_results.append(print_test_result("调试模式下执行命令", debug_solution_result))
    
    # 测试断开连接
    print("\n9. 断开连接测试...")
    if workstation.connected:
        disconnect_result = workstation.disconnect_device()
        test_results.append(print_test_result("断开设备连接", disconnect_result))
        if disconnect_result:
            test_results.append(print_test_result("检查断开状态", not workstation.connected))
    
    # 汇总测试结果
    print("\n" + "=" * 70)
    print("测试结果汇总")
    print("=" * 70)
    
    total_tests = len(test_results)
    passed_tests = sum(1 for result in test_results if result)
    failed_tests = total_tests - passed_tests
    
    print(f"总测试数: {total_tests}")
    print(f"通过测试: {passed_tests}")
    print(f"失败测试: {failed_tests}")
    
    success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
    print(f"成功率: {success_rate:.1f}%")
    
    print("\n" + "=" * 70)
    print("测试完成！")
    print("=" * 70)
    
    return passed_tests == total_tests


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)