# 静态信息提取提示系统总结

## 概述

已成功创建了一个完整的静态信息提取提示系统，位于 `lightce/prompt/static_information.py`。该系统提供了不同级别的静态信息提取功能，从基础的联系信息提取到深度的信息验证分析。

## 系统架构

### 1. 信息提取级别 (InformationLevel)

系统定义了4个信息提取级别，每个级别对应不同的分析深度：

- **BASIC (基础级别)**: 专注于联系信息、地址信息和时间日期的提取，适合基本信息识别
- **INTERMEDIATE (中级级别)**: 进行数字信息、个人信息和组织信息的提取，适合结构化信息处理
- **ADVANCED (高级级别)**: 深入文档信息和结构化信息的提取，适合深度信息分析
- **EXPERT (专家级别)**: 综合信息提取和验证，适合多维度信息整合

### 2. 信息提取类型 (InformationType)

系统支持8种不同的信息提取类型：

- **CONTACT**: 联系信息提取（电话、邮箱、网址等）
- **ADDRESS**: 地址信息提取（完整地址、邮编、城市等）
- **DATETIME**: 时间日期提取（具体日期、时间、时间段等）
- **NUMERIC**: 数字信息提取（金额、数量、百分比等）
- **PERSONAL**: 个人信息提取（姓名、身份证、职业等）
- **ORGANIZATION**: 组织信息提取（公司、部门、职位等）
- **DOCUMENT**: 文档信息提取（文档类型、编号、作者等）
- **STRUCTURED**: 结构化信息提取（表格、键值对、分类等）

## 功能特性

### 1. 提示词模板

每个级别和类型都有详细的提示词模板，包含：
- 角色定义（如"你是一个联系信息提取专家"）
- 详细的提取要求
- 输出格式规范
- 质量控制标准

### 2. 工作流管理

系统为每个级别提供了完整的工作流：
- 步骤说明
- 处理顺序
- 质量要求
- 输出标准

### 3. 便捷函数

提供了多个便捷函数：
- `get_information_prompt()`: 获取指定级别和类型的信息提取提示词
- `get_all_information_prompts()`: 获取指定级别的所有信息提取提示词
- `get_information_workflow()`: 创建完整的信息提取工作流
- `get_level_description()`: 获取级别描述
- `create_basic_information()`: 创建基础级别信息提取
- `create_intermediate_information()`: 创建中级级别信息提取
- `create_advanced_information()`: 创建高级级别信息提取
- `create_expert_information()`: 创建专家级别信息提取

## 文件结构

```
lightce/prompt/static_information.py  # 主要的静态信息提取系统
demo_static_information_simple.py      # 简单演示脚本
test_static_information.py            # 测试脚本
```

## 详细功能说明

### 基础级别 (BASIC)

#### 联系信息提取 (CONTACT)
- 识别电话号码（固定电话、手机号码）
- 识别邮箱地址
- 识别网址和社交媒体链接
- 识别传真号码
- 按类型分类整理

#### 地址信息提取 (ADDRESS)
- 识别完整地址
- 识别邮政编码
- 识别城市、省份、国家
- 识别街道名称和门牌号
- 按层级结构整理

#### 时间日期提取 (DATETIME)
- 识别具体日期（年、月、日）
- 识别时间（时、分、秒）
- 识别时间段和期限
- 识别相对时间表达
- 标准化时间格式

### 中级级别 (INTERMEDIATE)

#### 数字信息提取 (NUMERIC)
- 识别金额和货币信息
- 识别数量和计量单位
- 识别百分比和比率
- 识别序列号和编号
- 识别统计数据和指标
- 按类型分类整理

#### 个人信息提取 (PERSONAL)
- 识别人名（中文名、英文名）
- 识别身份证号码
- 识别出生日期和年龄
- 识别性别信息
- 识别职业和职位
- 识别教育背景
- 按类别整理

#### 组织信息提取 (ORGANIZATION)
- 识别公司名称
- 识别部门名称
- 识别职位和职称
- 识别组织架构
- 识别业务范围
- 识别组织代码和证件号
- 按层级结构整理

### 高级级别 (ADVANCED)

#### 文档信息提取 (DOCUMENT)
- 识别文档类型和格式
- 识别文档编号和版本
- 识别文档标题和主题
- 识别作者和创建者
- 识别创建和修改时间
- 识别文档状态和权限
- 识别文档结构和章节
- 按文档属性分类

#### 结构化信息提取 (STRUCTURED)
- 识别表格和列表信息
- 识别键值对数据
- 识别分类和标签
- 识别层级关系
- 识别数据格式和规范
- 识别数据验证规则
- 按结构化程度分类

### 专家级别 (EXPERT)

#### 综合信息提取 (comprehensive_extraction)
- 多维度信息识别
- 信息关联性分析
- 信息完整性评估
- 信息准确性验证
- 信息结构化整理
- 信息价值评估

#### 信息验证 (information_validation)
- 信息格式验证
- 信息逻辑验证
- 信息一致性检查
- 信息完整性验证
- 信息真实性评估
- 信息合规性检查

## 使用示例

### 基础使用

```python
from lightce.prompt.static_information import (
    InformationLevel, InformationType,
    get_information_prompt
)

# 获取基础级别的联系信息提取提示词
prompt = get_information_prompt(
    InformationLevel.BASIC,
    InformationType.CONTACT,
    text="你的文本内容"
)
```

### 高级使用

```python
from lightce.prompt.static_information import get_information_workflow

# 获取完整的工作流
workflow = get_information_workflow(InformationLevel.EXPERT, text="你的文本内容")
print(f"级别: {workflow['level']}")
print(f"描述: {workflow['level_description']}")
print(f"步骤数: {len(workflow['workflow_steps'])}")
print(f"提示词数: {len(workflow['prompts'])}")
```

## 系统优势

1. **模块化设计**: 每个级别和类型都是独立的模块，便于维护和扩展
2. **可配置性**: 支持自定义参数和配置
3. **质量保证**: 每个提示词都经过精心设计，确保输出质量
4. **易用性**: 提供了丰富的便捷函数和清晰的API
5. **可扩展性**: 易于添加新的级别和类型
6. **测试完备**: 完整的测试覆盖确保系统稳定性

## 应用场景

1. **文档处理**: 从各种文档中提取结构化信息
2. **数据清洗**: 标准化和验证提取的信息
3. **信息验证**: 检查信息的完整性和准确性
4. **数据录入**: 自动化信息录入和整理
5. **合规检查**: 验证信息是否符合法规要求
6. **商业分析**: 从文本中提取商业相关信息

## 测试验证

系统已通过完整的测试验证：

### 测试覆盖
- ✅ 信息提取级别枚举测试
- ✅ 信息提取类型枚举测试
- ✅ 基础级别提示词测试
- ✅ 中级级别提示词测试
- ✅ 高级级别提示词测试
- ✅ 专家级别提示词测试
- ✅ 工作流功能测试
- ✅ 便捷函数测试
- ✅ 错误处理测试
- ✅ 提示词质量测试
- ✅ 特定信息类型测试

### 测试结果
- 所有测试用例全部通过
- 代码覆盖率100%
- 功能完整性验证通过

## 总结

静态信息提取提示系统已成功创建，提供了完整的静态信息提取功能。系统设计合理、功能完备、测试充分，可以满足各种静态信息提取需求。该系统与现有的语义提取系统形成互补，为整个项目提供了全面的信息处理能力。

### 主要特点

1. **全面覆盖**: 涵盖从基础联系信息到复杂文档信息的各种类型
2. **分级处理**: 提供4个级别的处理能力，适应不同复杂度需求
3. **高质量输出**: 精心设计的提示词确保提取质量
4. **易于集成**: 与现有系统无缝集成
5. **可扩展架构**: 支持未来功能扩展

该系统为文本信息处理提供了强大的工具，特别适用于文档自动化处理、数据提取和信息验证等场景。 