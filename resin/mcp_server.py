"""
Resin 工作站 MCP 服务器

本模块提供用于控制 Resin 工作站设备的 MCP (Model Context Protocol) 服务器。
它将所有设备命令作为 MCP 工具暴露，可由 LLM 助手调用。

"""

from fastmcp import FastMCP

from resin_client import ResinWorkstation

# 全局工作站实例
_workstation = None


def get_workstation() -> ResinWorkstation:
    """
    获取或创建全局工作站实例。

    返回:
        ResinWorkstation: 工作站实例
    """
    global _workstation
    if _workstation is None:
        _workstation = ResinWorkstation(
            address="127.0.0.1",
            port=8889,
            debug_mode=False
        )
    return _workstation


# 创建 FastMCP 服务器实例
mcp = FastMCP(
    name="resin-workstation-server",
    instructions="用于控制 Resin 工作站的 MCP 服务器。支持设备连接、溶液处理、反应器控制等功能。"
)


# ============================================================================
# 设备连接管理
# ============================================================================

@mcp.tool()
async def connect_device(
    address: str = "127.0.0.1",
    port: int = 8889
) -> str:
    """
    连接到 Resin 工作站设备（通过 UDP）。

    在执行任何其他操作之前，应首先调用此方法。

    Args:
        address: 设备 IP 地址（默认: 127.0.0.1）
        port: 设备端口（默认: 8889）

    Returns:
        连接结果信息（JSON 格式）
    """
    import json
    workstation = get_workstation()
    success = workstation.connect_device(address, port)
    status = workstation.device_status

    if success:
        result = {
            "status": "success",
            "message": f"成功连接到设备 {address}:{port}",
            "address": address,
            "port": port,
            "device_status": status
        }
    else:
        result = {
            "status": "error",
            "message": f"连接到设备 {address}:{port} 失败",
            "address": address,
            "port": port
        }

    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
async def disconnect_device() -> str:
    """
    断开与 Resin 工作站设备的连接。

    Returns:
        断开连接结果信息（JSON 格式）
    """
    import json
    workstation = get_workstation()
    success = workstation.disconnect_device()

    if success:
        result = {
            "status": "success",
            "message": "已成功断开设备连接"
        }
    else:
        result = {
            "status": "error",
            "message": "断开设备连接失败"
        }

    return json.dumps(result, ensure_ascii=False, indent=2)

# ============================================================================
# 状态查询 TODO: 当前获取状态未实现
# ============================================================================

@mcp.tool()
async def get_device_status() -> str:
    """
    获取完整的设备状态。

    包括连接状态、操作模式、所有反应器状态和后处理系统状态。

    Returns:
        设备状态信息（JSON 格式）
    """
    import json
    workstation = get_workstation()
    status = workstation.device_status
    return json.dumps(status, ensure_ascii=False, indent=2)


# ============================================================================
# 移液操作
# ============================================================================

@mcp.tool()
async def reactor_solution_add(
    solution_id: int,
    volume: float,
    reactor_id: int
) -> str:
    """
    向反应器添加溶液。

    从溶液瓶向指定反应器分配液体。

    Args:
        solution_id: 溶液瓶 ID（1-16）
        volume: 要添加的体积（毫升）
        reactor_id: 目标反应器 ID

    Returns:
        操作结果信息（JSON 格式）
    """
    import json
    workstation = get_workstation()
    result = workstation.reactor_solution_add(solution_id, volume, reactor_id)

    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
async def post_process_solution_add(
    start_bottle: str,
    end_bottle: str,
    volume: float,
    inject_speed: float,
    suck_speed: float = 4.0
) -> str:
    """
    在后处理系统中的瓶子之间转移溶液。

    将液体从一个瓶子移动到另一个瓶子。

    Args:
        start_bottle: 源瓶名称（如 'bottle1'、'bottle2'）
        end_bottle: 目标瓶名称
        volume: 要转移的体积（毫升）
        inject_speed: 注射速度（毫升/秒）
        suck_speed: 吸液速度（毫升/秒，默认: 4.0）

    Returns:
        操作结果信息（JSON 格式）
    """
    import json
    workstation = get_workstation()
    result = workstation.post_process_solution_add(
        start_bottle, end_bottle, volume, inject_speed, suck_speed
    )

    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
async def post_process_clean(post_process_id: int) -> str:
    """
    运行后处理系统的自动清洗程序。

    清洗管路和组件。

    Args:
        post_process_id: 后处理系统 ID

    Returns:
        操作结果信息（JSON 格式）
    """
    import json
    workstation = get_workstation()
    result = workstation.post_process_clean(post_process_id)

    return json.dumps(result, ensure_ascii=False, indent=2)


# ============================================================================
# 反应器气体控制
# ============================================================================

@mcp.tool()
async def reactor_n2_on(reactor_id: int) -> str:
    """
    打开反应器的氮气通流。

    氮气用于惰性气氛控制。

    Args:
        reactor_id: 反应器 ID

    Returns:
        操作结果信息（JSON 格式）
    """
    import json
    workstation = get_workstation()
    result = workstation.reactor_n2_on(reactor_id)

    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
async def reactor_n2_off(reactor_id: int) -> str:
    """
    关闭反应器的氮气通流。

    Args:
        reactor_id: 反应器 ID

    Returns:
        操作结果信息（JSON 格式）
    """
    import json
    workstation = get_workstation()
    result = workstation.reactor_n2_off(reactor_id)

    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
async def reactor_air_on(reactor_id: int) -> str:
    """
    打开反应器的空气通流。

    空气用于曝气或冷却。

    Args:
        reactor_id: 反应器 ID

    Returns:
        操作结果信息（JSON 格式）
    """
    import json
    workstation = get_workstation()
    result = workstation.reactor_air_on(reactor_id)

    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
async def reactor_air_off(reactor_id: int) -> str:
    """
    关闭反应器的空气通流。

    Args:
        reactor_id: 反应器 ID

    Returns:
        操作结果信息（JSON 格式）
    """
    import json
    workstation = get_workstation()
    result = workstation.reactor_air_off(reactor_id)

    return json.dumps(result, ensure_ascii=False, indent=2)


# ============================================================================
# 温度控制
# ============================================================================

@mcp.tool()
async def temp_set(reactor_id: int, temperature: float) -> str:
    """
    设置反应器的目标温度。

    反应器将加热或冷却以达到此温度。

    Args:
        reactor_id: 反应器 ID
        temperature: 目标温度（摄氏度）

    Returns:
        操作结果信息（JSON 格式）
    """
    import json
    workstation = get_workstation()
    result = workstation.temp_set(reactor_id, temperature)

    return json.dumps(result, ensure_ascii=False, indent=2)


# ============================================================================
# 搅拌控制
# ============================================================================

@mcp.tool()
async def start_reactor_stirrer(reactor_id: int, speed: float) -> str:
    """
    以指定速度启动反应器的搅拌器。

    Args:
        reactor_id: 反应器 ID
        speed: 搅拌速度（RPM）

    Returns:
        操作结果信息（JSON 格式）
    """
    import json
    workstation = get_workstation()
    result = workstation.start_reactor_stirrer(reactor_id, speed)

    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
async def stop_reactor_stirrer(reactor_id: int) -> str:
    """
    停止反应器的搅拌器。

    Args:
        reactor_id: 反应器 ID

    Returns:
        操作结果信息（JSON 格式）
    """
    import json
    workstation = get_workstation()
    result = workstation.stop_reactor_stirrer(reactor_id)

    return json.dumps(result, ensure_ascii=False, indent=2)


# ============================================================================
# 排液控制
# ============================================================================

@mcp.tool()
async def post_process_discharge_on(post_process_id: int) -> str:
    """
    打开后处理系统的排液阀以排出液体。

    Args:
        post_process_id: 后处理系统 ID

    Returns:
        操作结果信息（JSON 格式）
    """
    import json
    workstation = get_workstation()
    result = workstation.post_process_discharge_on(post_process_id)

    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
async def post_process_discharge_off(post_process_id: int) -> str:
    """
    关闭后处理系统的排液阀。

    Args:
        post_process_id: 后处理系统 ID

    Returns:
        操作结果信息（JSON 格式）
    """
    import json
    workstation = get_workstation()
    result = workstation.post_process_discharge_off(post_process_id)

    return json.dumps(result, ensure_ascii=False, indent=2)


# ============================================================================
# 工具函数
# ============================================================================

@mcp.tool()
async def wait(seconds: int) -> str:
    """
    等待指定的秒数。

    用于在操作之间添加延时。

    Args:
        seconds: 等待秒数

    Returns:
        操作结果信息
    """
    workstation = get_workstation()
    success = workstation.wait(seconds)

    if success:
        return f"✓ 已等待 {seconds} 秒"
    else:
        return "✗ 等待操作失败"


# ============================================================================
# 主程序入口
# ============================================================================

def main():
    """
    MCP 服务器的主入口点。
    """
    # 初始化全局工作站实例
    global _workstation
    _workstation = ResinWorkstation(
        address="127.0.0.1",
        port=8888,
        debug_mode=False
    )

    # 运行服务器，指定端口
    mcp.run(transport="streamable-http", port=8000, host="0.0.0.0")


if __name__ == "__main__":
    main()
