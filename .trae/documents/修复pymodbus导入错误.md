## 修复pymodbus导入错误

### 问题分析
1. **错误信息**：`ImportError: cannot import name 'Endian' from 'pymodbus.constants'`
2. **问题位置**：`inovance_three_axis.py` 文件第6行
3. **根本原因**：
   - 当前pymodbus版本中，`Endian` 常量已从 `pymodbus.constants` 模块移除
   - 该导入在代码中实际上没有被使用

### 修复方案
1. **删除未使用的导入**：移除 `from pymodbus.constants import Endian` 这行代码
2. **验证修复**：确保程序能够正常运行

### 修复步骤
1. 编辑 `C:\Users\dell\Desktop\Resin_Project\resin\Drivers\EthernetDevices\inovance_three_axis\inovance_three_axis.py` 文件
2. 删除第6行 `from pymodbus.constants import Endian`
3. 保存文件并运行程序验证修复效果

### 预期结果
- 程序不再报导入错误
- 所有功能正常运行

### 技术说明
- 这是一个版本兼容性问题，旧版本pymodbus中`Endian`可能存在于constants模块中
- 由于该导入未被实际使用，删除它不会影响任何功能
- 修复后程序将能够在当前pymodbus版本下正常运行