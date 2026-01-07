# 实现SQLite数据库存储和执行功能（修订版）

## 1. 数据库设计
- 在项目根目录创建SQLite数据库文件 `process_db.db`
- 设计 `process_files` 表，包含以下字段：
  - `id`：主键，自增整数
  - `filename`：文件名，文本类型
  - `content`：文件内容，文本类型
  - `import_time`：导入时间，时间戳类型
  - `is_active`：是否为当前活跃文件，布尔类型

## 2. 代码修改计划

### 2.1 创建新的数据库操作文件
- 在 `ActionSequence` 目录下创建 `database_manager.py` 文件
- 实现所有数据库相关操作函数：
  - 导入 `sqlite3` 和 `datetime` 模块
  - `init_database()`：初始化数据库连接和表结构
  - `save_process_file(filename, content)`：保存工艺文件到数据库
  - `get_active_process_file()`：获取当前活跃的工艺文件
  - `set_active_file(file_id)`：设置指定文件为活跃状态

### 2.2 修改 `execute_sequence.py` 文件
1. **导入数据库操作模块**：
   - 导入 `database_manager` 模块
   - 确保数据库初始化

2. **修改 `Import_Process_Bond` 函数**：
   - 在读取txt文件后，调用 `database_manager.save_process_file()` 将文件内容保存到数据库
   - 保存文件名、完整内容和导入时间

3. **添加 `Execute_Bond` 函数**：
   - 调用 `database_manager.get_active_process_file()` 获取当前活跃的工艺文件
   - 将内容写入临时txt文件
   - 使用 `generate_execution_sequence` 函数解析临时文件
   - 使用 `execute_sequence` 函数执行解析后的序列
   - 清理临时文件

## 3. 实现步骤
1. 创建 `database_manager.py` 文件，编写数据库操作函数
2. 修改 `execute_sequence.py` 文件，导入数据库模块
3. 更新 `Import_Process_Bond` 函数，添加数据库保存功能
4. 编写 `Execute_Bond` 函数，实现从数据库读取和执行功能
5. 测试功能完整性

## 4. 预期效果
- 用户通过导入按钮选择txt文件后，文件内容将保存到数据库
- 点击执行按钮时，系统将从数据库读取当前活跃的工艺文件并执行
- 数据库将记录所有导入的工艺文件，支持历史记录管理
- 数据库操作与业务逻辑分离，提高代码的可维护性

## 5. 注意事项
- 使用SQLite的事务确保数据一致性
- 处理临时文件的创建和清理，避免资源泄漏
- 确保数据库操作的异常处理，提高系统健壮性
- 保持代码的可维护性和可读性
- 确保新文件的导入路径正确，符合项目的模块结构