#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
结构化排序工具演示
展示如何使用UniversalAgent来完成结构化输入的内容提取和输出功能
"""

import json
from lightce.tools.structure_sort import (
    StructureSortAgent, StructureSortConfig,
    create_structure_sort_agent, process_structure_with_agent,
    StructureSortTool, StructureType, SortOrder
)

def demo_json_processing():
    """演示JSON数据处理"""
    print("=" * 60)
    print("JSON数据处理演示")
    print("=" * 60)
    
    test_json = """
    {
        "users": [
            {"id": 3, "name": "张三", "age": 28, "priority": "high", "department": "技术部"},
            {"id": 1, "name": "李四", "age": 32, "priority": "medium", "department": "产品部"},
            {"id": 2, "name": "王五", "age": 25, "priority": "low", "department": "设计部"},
            {"id": 4, "name": "赵六", "age": 35, "priority": "high", "department": "技术部"}
        ]
    }
    """
    
    # 创建JSON处理代理
    agent = create_structure_sort_agent("json", "ascending")
    
    # 执行处理
    result = agent.process_structure(test_json, "id")
    
    print(f"输入数据: {test_json.strip()}")
    print(f"结构类型: {result.structure_type}")
    print(f"排序顺序: {result.sort_order}")
    print(f"成功状态: {result.success}")
    print(f"处理时间: {result.processing_time:.2f}秒")
    print(f"提取统计: {result.extraction_stats}")
    
    if result.success:
        print("\n提取的内容:")
        print(json.dumps(result.extracted_content, ensure_ascii=False, indent=2))
        
        print("\n排序后的内容:")
        print(json.dumps(result.sorted_content, ensure_ascii=False, indent=2))
        
        print("\n格式化输出:")
        print(result.formatted_output)

def demo_xml_processing():
    """演示XML数据处理"""
    print("\n" + "=" * 60)
    print("XML数据处理演示")
    print("=" * 60)
    
    test_xml = """
    <employees>
        <employee id="3" name="张三" age="28" department="技术部">
            <skills>
                <skill>Python</skill>
                <skill>Java</skill>
            </skills>
        </employee>
        <employee id="1" name="李四" age="32" department="产品部">
            <skills>
                <skill>产品设计</skill>
                <skill>用户研究</skill>
            </skills>
        </employee>
        <employee id="2" name="王五" age="25" department="设计部">
            <skills>
                <skill>UI设计</skill>
                <skill>平面设计</skill>
            </skills>
        </employee>
    </employees>
    """
    
    # 创建XML处理代理
    agent = create_structure_sort_agent("xml", "alphabetical")
    
    # 执行处理
    result = agent.process_structure(test_xml, "name")
    
    print(f"输入数据: {test_xml.strip()}")
    print(f"结构类型: {result.structure_type}")
    print(f"排序顺序: {result.sort_order}")
    print(f"成功状态: {result.success}")
    print(f"处理时间: {result.processing_time:.2f}秒")
    
    if result.success:
        print("\n提取的内容:")
        print(json.dumps(result.extracted_content, ensure_ascii=False, indent=2))
        
        print("\n排序后的内容:")
        print(json.dumps(result.sorted_content, ensure_ascii=False, indent=2))
        
        print("\n格式化输出:")
        print(result.formatted_output)

def demo_csv_processing():
    """演示CSV数据处理"""
    print("\n" + "=" * 60)
    print("CSV数据处理演示")
    print("=" * 60)
    
    test_csv = """
    姓名,年龄,部门,薪资,入职日期
    张三,28,技术部,15000,2020-03-15
    李四,32,产品部,18000,2018-06-01
    王五,25,设计部,12000,2021-09-10
    赵六,35,技术部,20000,2017-12-01
    """
    
    # 创建CSV处理代理
    agent = create_structure_sort_agent("csv", "numerical")
    
    # 执行处理
    result = agent.process_structure(test_csv, "薪资")
    
    print(f"输入数据: {test_csv.strip()}")
    print(f"结构类型: {result.structure_type}")
    print(f"排序顺序: {result.sort_order}")
    print(f"成功状态: {result.success}")
    print(f"处理时间: {result.processing_time:.2f}秒")
    
    if result.success:
        print("\n提取的内容:")
        print(json.dumps(result.extracted_content, ensure_ascii=False, indent=2))
        
        print("\n排序后的内容:")
        print(json.dumps(result.sorted_content, ensure_ascii=False, indent=2))
        
        print("\n格式化输出:")
        print(result.formatted_output)

def demo_table_processing():
    """演示表格数据处理"""
    print("\n" + "=" * 60)
    print("表格数据处理演示")
    print("=" * 60)
    
    test_table = """
    | 项目名称 | 负责人 | 优先级 | 完成度 | 截止日期 |
    |---------|--------|--------|--------|----------|
    | 用户系统 | 张三   | 高     | 80%    | 2024-01-15 |
    | 支付模块 | 李四   | 中     | 60%    | 2024-02-01 |
    | 数据统计 | 王五   | 低     | 90%    | 2024-01-30 |
    | 移动端   | 赵六   | 高     | 70%    | 2024-02-15 |
    """
    
    # 创建表格处理代理
    agent = create_structure_sort_agent("table", "priority")
    
    # 执行处理
    result = agent.process_structure(test_table, "优先级")
    
    print(f"输入数据: {test_table.strip()}")
    print(f"结构类型: {result.structure_type}")
    print(f"排序顺序: {result.sort_order}")
    print(f"成功状态: {result.success}")
    print(f"处理时间: {result.processing_time:.2f}秒")
    
    if result.success:
        print("\n提取的内容:")
        print(json.dumps(result.extracted_content, ensure_ascii=False, indent=2))
        
        print("\n排序后的内容:")
        print(json.dumps(result.sorted_content, ensure_ascii=False, indent=2))
        
        print("\n格式化输出:")
        print(result.formatted_output)

def demo_list_processing():
    """演示列表数据处理"""
    print("\n" + "=" * 60)
    print("列表数据处理演示")
    print("=" * 60)
    
    test_list = """
    - 项目A：用户管理系统开发
    - 项目B：支付系统集成
    - 项目C：数据分析平台
    - 项目D：移动端应用开发
    - 项目E：API接口优化
    """
    
    # 创建列表处理代理
    agent = create_structure_sort_agent("list", "alphabetical")
    
    # 执行处理
    result = agent.process_structure(test_list)
    
    print(f"输入数据: {test_list.strip()}")
    print(f"结构类型: {result.structure_type}")
    print(f"排序顺序: {result.sort_order}")
    print(f"成功状态: {result.success}")
    print(f"处理时间: {result.processing_time:.2f}秒")
    
    if result.success:
        print("\n提取的内容:")
        print(json.dumps(result.extracted_content, ensure_ascii=False, indent=2))
        
        print("\n排序后的内容:")
        print(json.dumps(result.sorted_content, ensure_ascii=False, indent=2))
        
        print("\n格式化输出:")
        print(result.formatted_output)

def demo_tree_processing():
    """演示树形数据处理"""
    print("\n" + "=" * 60)
    print("树形数据处理演示")
    print("=" * 60)
    
    test_tree = """
    公司
    ├─ 技术部
    │   ├─ 前端组
    │   │   ├─ 张三
    │   │   └─ 李四
    │   └─ 后端组
    │       ├─ 王五
    │       └─ 赵六
    ├─ 产品部
    │   ├─ 产品组
    │   │   ├─ 孙七
    │   │   └─ 周八
    │   └─ 设计组
    │       ├─ 吴九
    │       └─ 郑十
    └─ 运营部
        ├─ 市场组
        │   ├─ 陈十一
        │   └─ 林十二
        └─ 客服组
            ├─ 黄十三
            └─ 刘十四
    """
    
    # 创建树形处理代理
    agent = create_structure_sort_agent("tree", "alphabetical")
    
    # 执行处理
    result = agent.process_structure(test_tree)
    
    print(f"输入数据: {test_tree.strip()}")
    print(f"结构类型: {result.structure_type}")
    print(f"排序顺序: {result.sort_order}")
    print(f"成功状态: {result.success}")
    print(f"处理时间: {result.processing_time:.2f}秒")
    
    if result.success:
        print("\n提取的内容:")
        print(json.dumps(result.extracted_content, ensure_ascii=False, indent=2))
        
        print("\n排序后的内容:")
        print(json.dumps(result.sorted_content, ensure_ascii=False, indent=2))
        
        print("\n格式化输出:")
        print(result.formatted_output)

def demo_graph_processing():
    """演示图数据处理"""
    print("\n" + "=" * 60)
    print("图数据处理演示")
    print("=" * 60)
    
    test_graph = """
    节点A -> 节点B
    节点A -> 节点C
    节点B -> 节点D
    节点C -> 节点D
    节点C -> 节点E
    节点D -> 节点F
    节点E -> 节点F
    """
    
    # 创建图处理代理
    agent = create_structure_sort_agent("graph", "alphabetical")
    
    # 执行处理
    result = agent.process_structure(test_graph)
    
    print(f"输入数据: {test_graph.strip()}")
    print(f"结构类型: {result.structure_type}")
    print(f"排序顺序: {result.sort_order}")
    print(f"成功状态: {result.success}")
    print(f"处理时间: {result.processing_time:.2f}秒")
    
    if result.success:
        print("\n提取的内容:")
        print(json.dumps(result.extracted_content, ensure_ascii=False, indent=2))
        
        print("\n排序后的内容:")
        print(json.dumps(result.sorted_content, ensure_ascii=False, indent=2))
        
        print("\n格式化输出:")
        print(result.formatted_output)

def demo_batch_processing():
    """演示批量处理"""
    print("\n" + "=" * 60)
    print("批量处理演示")
    print("=" * 60)
    
    input_data_list = [
        '{"items": [{"id": 3, "name": "项目A"}, {"id": 1, "name": "项目B"}]}',
        '<data><item id="2">项目C</item><item id="1">项目D</item></data>',
        'name,age\n张三,28\n李四,32'
    ]
    
    custom_sort_keys = ["id", "id", "age"]
    
    # 创建代理
    agent = create_structure_sort_agent("json", "ascending")
    
    # 批量处理
    results = agent.batch_process(input_data_list, custom_sort_keys)
    
    print(f"批量处理 {len(input_data_list)} 个数据")
    
    for i, result in enumerate(results):
        print(f"\n--- 数据 {i+1} ---")
        print(f"成功: {result.success}")
        print(f"结构类型: {result.structure_type}")
        print(f"处理时间: {result.processing_time:.2f}秒")
        
        if result.success:
            print(f"提取统计: {result.extraction_stats}")
            print(f"格式化输出: {result.formatted_output[:100]}...")

def demo_langchain_tool():
    """演示LangChain工具包装器"""
    print("\n" + "=" * 60)
    print("LangChain工具包装器演示")
    print("=" * 60)
    
    test_data = """
    {
        "products": [
            {"id": 3, "name": "产品A", "price": 100, "category": "电子产品"},
            {"id": 1, "name": "产品B", "price": 50, "category": "服装"},
            {"id": 2, "name": "产品C", "price": 200, "category": "电子产品"}
        ]
    }
    """
    
    # 创建结构化排序代理
    agent = create_structure_sort_agent("json", "descending")
    
    # 创建LangChain工具
    tool = StructureSortTool(agent)
    
    # 使用工具进行处理
    result = tool._run(
        input_data=test_data,
        structure_type="json",
        sort_order="descending",
        custom_sort_key="price"
    )
    
    print(f"输入数据: {test_data.strip()}")
    print(f"工具名称: {tool.name}")
    print(f"工具描述: {tool.description}")
    print(f"执行结果: {result['success']}")
    
    if result['success']:
        print(f"结构类型: {result['structure_type']}")
        print(f"排序顺序: {result['sort_order']}")
        print(f"处理时间: {result['processing_time']:.2f}秒")
        print(f"提取统计: {result['extraction_stats']}")
        
        print("\n格式化输出:")
        print(result['formatted_output'])

def demo_statistics():
    """演示统计信息"""
    print("\n" + "=" * 60)
    print("统计信息演示")
    print("=" * 60)
    
    # 创建代理
    agent = create_structure_sort_agent("json", "ascending")
    
    # 执行多次处理
    test_data_list = [
        '{"items": [{"id": 3, "name": "A"}, {"id": 1, "name": "B"}]}',
        '{"items": [{"id": 2, "name": "C"}, {"id": 4, "name": "D"}]}',
        '{"items": [{"id": 5, "name": "E"}, {"id": 0, "name": "F"}]}'
    ]
    
    for data in test_data_list:
        agent.process_structure(data, "id")
    
    # 获取统计信息
    stats = agent.get_statistics()
    
    print("处理统计信息:")
    print(f"总处理次数: {stats['total_processings']}")
    print(f"成功处理次数: {stats['successful_processings']}")
    print(f"成功率: {stats['success_rate']:.2%}")
    print(f"平均处理时间: {stats['average_processing_time']:.2f}秒")
    
    print("\n类型统计:")
    for structure_type, type_stats in stats['type_statistics'].items():
        print(f"  {structure_type}: {type_stats['count']}次, 平均时间: {type_stats['avg_time']:.2f}秒")

def demo_advanced_configuration():
    """演示高级配置"""
    print("\n" + "=" * 60)
    print("高级配置演示")
    print("=" * 60)
    
    test_data = """
    {
        "tasks": [
            {"id": 3, "name": "紧急任务A", "priority": "high", "deadline": "2024-01-15"},
            {"id": 1, "name": "普通任务B", "priority": "medium", "deadline": "2024-02-01"},
            {"id": 2, "name": "一般任务C", "priority": "low", "deadline": "2024-01-30"}
        ]
    }
    """
    
    # 创建自定义配置
    from lightce.agent.system import ModelConfig
    
    model_config = ModelConfig(
        model_name="gpt-4",
        temperature=0.1,
        max_tokens=2000,
        provider="openai"
    )
    
    config = StructureSortConfig(
        structure_type=StructureType.JSON,
        sort_order=SortOrder.PRIORITY,
        model_config=model_config,
        enable_extraction=True,
        enable_sorting=True,
        enable_formatting=True,
        custom_sort_key="priority",
        max_items=5
    )
    
    # 创建代理
    agent = StructureSortAgent(config)
    
    # 执行处理
    result = agent.process_structure(test_data, "priority")
    
    print(f"配置信息:")
    print(f"  结构类型: {config.structure_type.value}")
    print(f"  排序顺序: {config.sort_order.value}")
    print(f"  模型配置: {config.model_config.dict()}")
    print(f"  启用提取: {config.enable_extraction}")
    print(f"  启用排序: {config.enable_sorting}")
    print(f"  启用格式化: {config.enable_formatting}")
    print(f"  自定义排序键: {config.custom_sort_key}")
    print(f"  最大项目数: {config.max_items}")
    
    print(f"\n处理结果:")
    print(f"成功: {result.success}")
    print(f"处理时间: {result.processing_time:.2f}秒")
    print(f"提取统计: {result.extraction_stats}")
    
    if result.success:
        print("\n格式化输出:")
        print(result.formatted_output)

def demo_different_sort_orders():
    """演示不同排序顺序"""
    print("\n" + "=" * 60)
    print("不同排序顺序演示")
    print("=" * 60)
    
    test_data = """
    {
        "items": [
            {"id": 3, "name": "张三", "age": 28, "priority": "high", "date": "2024-01-15"},
            {"id": 1, "name": "李四", "age": 32, "priority": "medium", "date": "2024-02-01"},
            {"id": 2, "name": "王五", "age": 25, "priority": "low", "date": "2024-01-30"},
            {"id": 4, "name": "赵六", "age": 35, "priority": "high", "date": "2024-01-10"}
        ]
    }
    """
    
    sort_orders = [
        ("ascending", "id", "升序排序"),
        ("descending", "id", "降序排序"),
        ("alphabetical", "name", "字母排序"),
        ("numerical", "age", "数值排序"),
        ("chronological", "date", "时间排序"),
        ("priority", "priority", "优先级排序")
    ]
    
    for sort_order, sort_key, description in sort_orders:
        print(f"\n--- {description} ---")
        
        agent = create_structure_sort_agent("json", sort_order)
        result = agent.process_structure(test_data, sort_key)
        
        print(f"排序顺序: {result.sort_order}")
        print(f"排序键: {sort_key}")
        print(f"成功: {result.success}")
        
        if result.success:
            print("排序结果:")
            for item in result.sorted_content:
                if isinstance(item, dict):
                    print(f"  {item.get('name', 'Unknown')} (ID: {item.get('id', 'N/A')})")

def main():
    """主演示函数"""
    print("结构化排序工具演示")
    print("=" * 60)
    
    while True:
        print("\n请选择演示功能:")
        print("1. JSON数据处理")
        print("2. XML数据处理")
        print("3. CSV数据处理")
        print("4. 表格数据处理")
        print("5. 列表数据处理")
        print("6. 树形数据处理")
        print("7. 图数据处理")
        print("8. 批量处理")
        print("9. LangChain工具包装器")
        print("10. 统计信息")
        print("11. 高级配置")
        print("12. 不同排序顺序")
        print("0. 退出")
        
        choice = input("\n请输入选择 (0-12): ").strip()
        
        if choice == "0":
            print("感谢使用结构化排序工具演示！")
            break
        elif choice == "1":
            demo_json_processing()
        elif choice == "2":
            demo_xml_processing()
        elif choice == "3":
            demo_csv_processing()
        elif choice == "4":
            demo_table_processing()
        elif choice == "5":
            demo_list_processing()
        elif choice == "6":
            demo_tree_processing()
        elif choice == "7":
            demo_graph_processing()
        elif choice == "8":
            demo_batch_processing()
        elif choice == "9":
            demo_langchain_tool()
        elif choice == "10":
            demo_statistics()
        elif choice == "11":
            demo_advanced_configuration()
        elif choice == "12":
            demo_different_sort_orders()
        else:
            print("无效的选择，请重新输入")

if __name__ == "__main__":
    main() 