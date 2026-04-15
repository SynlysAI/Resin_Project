# fastapi_service 接口文档

本文档对应文件：`E:/xx_project/Resin_Project/fastapi_service.py`

## 1. 服务信息

- 基础地址：`http://<host>:8000`
- 默认启动：`uvicorn fastapi_service:app --host 0.0.0.0 --port 8000`
- 响应时间字段：`timestamp` / `generated_at` 为 UTC ISO8601 字符串

## 2. 接口总览

1. `GET /health`：健康检查
2. `POST /api/v1/experiment/trigger`：异步触发本地实验指令解析
3. `POST /api/v1/experiment/execute`：执行工艺流程（仅在 trigger 任务完成后可调用）
4. `GET /api/v1/experiment/status`：查询执行状态

## 3. 通用响应模型（ApiResponse）

```json
{
  "ok": true,
  "message": "说明信息",
  "request_id": "请求ID",
  "signal": "信号名",
  "udp_ack": {},
  "timestamp": "2026-04-08T12:34:56.789012"
}
```

字段说明：

- `ok`: 是否成功
- `message`: 中文说明
- `request_id`: 请求标识（客户端可传，未传则服务端生成 UUID）
- `signal`: 本次操作对应的内部信号
- `udp_ack`: UDP 返回内容（若无则为 `null`）
- `timestamp`: 响应生成时间（UTC）

## 4. 详细接口

### 4.1 健康检查

- 方法：`GET`
- 路径：`/health`

成功响应示例：

```json
{
  "ok": true,
  "service": "smartcmd-fastapi",
  "udp_target": {
    "host": "127.0.0.1",
    "port": 8889
  },
  "timestamp": "2026-04-08T12:34:56.789012"
}
```

### 4.2 触发实验指令解析（异步）

- 方法：`POST`
- 路径：`/api/v1/experiment/trigger`
- 说明：
1. 接收实验参数 `experiment_plan`
2. 异步执行本地方法 `Tools.trigger_parser.handle_generate_instructions(experiment_plan)`
3. 任务未完成前，`/api/v1/experiment/execute` 会返回 `409`

请求体：

```json
{
  "experiment_plan": "实验参数文本",
  "request_id": "可选请求ID"
}
```

请求字段：

- `experiment_plan` (string, 必填, min_length=1): 实验方案文本
- `request_id` (string, 选填): 外部请求 ID

成功响应（200）示例：

```json
{
  "ok": true,
  "message": "本地指令解析任务已异步启动，完成后才能调用 execute 接口。",
  "request_id": "f87f4f2f-4e8f-48ea-bb8b-e5f2b1619e2e",
  "signal": "TRIGGER_GENERATE_LOCAL",
  "udp_ack": null,
  "timestamp": "2026-04-08T12:34:56.789012"
}
```

失败响应：

- `409 Conflict`：上一轮指令解析任务仍在执行中

### 4.3 执行工艺流程

- 方法：`POST`
- 路径：`/api/v1/experiment/execute`
- 说明：仅当 trigger 触发的解析任务完成且成功后才允许执行

请求体（可空）：

```json
{
  "request_id": "可选请求ID"
}
```

成功响应（200）示例：

```json
{
  "ok": true,
  "message": "工艺流程执行命令已下发，请通过 /api/v1/experiment/status 查询进度。",
  "request_id": "2e0ab3df-8ea5-4f30-a5ca-3e9c8388f910",
  "signal": "EXECUTE_PROCESS_FILE",
  "udp_ack": {
    "status": "success",
    "command": "EXECUTE_PROCESS_FILE"
  },
  "timestamp": "2026-04-08T12:36:00.123456"
}
```

失败响应：

- `409 Conflict`：
1. 未先调用 trigger
2. 指令解析仍在执行中
3. 指令解析尚未完成
4. 指令解析失败
- `502 Bad Gateway`：调用 UDP 执行服务失败（`EXECUTE_PROCESS_FILE`）

### 4.4 查询执行状态

- 方法：`GET`
- 路径：`/api/v1/experiment/status`
- 说明：查询 `GET_PROCESS_EXECUTION_STATE` 并返回当前执行状态

成功响应示例：

```json
{
  "ok": true,
  "request_id": "2e0ab3df-8ea5-4f30-a5ca-3e9c8388f910",
  "status": "running",
  "detail": "process=control_instructions, step=21/34, current_command=Add_Solution_to_Reactor, executing=True",
  "current_command": "Add_Solution_to_Reactor",
  "last_plan_updated_at": "2026-04-08T12:34:56.789012",
  "last_triggered_at": "2026-04-08T12:34:56.789012",
  "generated_at": "2026-04-08T12:36:05.456789"
}
```

字段补充说明：

- `current_command`：当前执行步骤的命令名（来自执行线程当前步骤函数名）
- 当当前步骤命令为 `Wait` 时，不会覆盖 `current_command`，会保留上一条非 `Wait` 的命令名

`status` 可能值：

- `running`：流程正在执行
- `success`：当前无流程执行（`executing=False`）

失败响应：

- `502 Bad Gateway`：调用 UDP 状态服务失败，或返回格式不符合预期

## 5. 调用时序建议

1. 调用 `POST /api/v1/experiment/trigger` 提交实验参数并启动解析
2. 等待解析完成（可结合业务等待或重试 `execute`）
3. 调用 `POST /api/v1/experiment/execute` 启动流程执行
4. 调用 `GET /api/v1/experiment/status` 轮询执行进度

## 6. 兼容性说明

以下旧接口已不再提供：

1. `/api/v1/experiment/plan`
2. `/api/v1/experiment/generation-complete`
