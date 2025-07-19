#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
结构化排序工具测试
验证结构化排序工具的各种功能
"""

import unittest
from unittest.mock import patch, MagicMock
import time
import json
import re

from lightce.tools.structure_sort import (
    StructureSortAgent, StructureSortConfig,
    StructureSortResult, StructureSortTool,
    create_structure_sort_agent, process_structure_with_agent,
    StructureType, SortOrder
)
from lightce.agent.system import ModelConfig

class TestStructureSortTool(unittest.TestCase):
    """结构化排序工具测试类"""
    
    def setUp(self):
        """测试前的准备工作"""
        self.test_json = """
        {
            "users": [
                {"id": 3, "name": "张三", "age": 28, "priority": "high"},
                {"id": 1, "name": "李四", "age": 32, "priority": "medium"},
                {"id": 2, "name": "王五", "age": 25, "priority": "low"}
            ]
        }
        """
        
        self.test_xml = """
        <employees>
            <employee id="3" name="张三" age="28"/>
            <employee id="1" name="李四" age="32"/>
            <employee id="2" name="王五" age="25"/>
        </employees>
        """
        
        self.test_csv = """
        姓名,年龄,部门
        张三,28,技术部
        李四,32,产品部
        王五,25,设计部
        """
    
    def test_structure_sort_config(self):
        """测试结构化排序配置"""
        config = StructureSortConfig()
        
        self.assertEqual(config.structure_type, StructureType.JSON)
        self.assertEqual(config.sort_order, SortOrder.ASCENDING)
        self.assertIsNone(config.model_config)
        self.assertTrue(config.enable_extraction)
        self.assertTrue(config.enable_sorting)
        self.assertTrue(config.enable_formatting)
        self.assertIsNone(config.custom_sort_key)
        self.assertIsNone(config.max_items)
    
    def test_structure_sort_result(self):
        """测试结构化排序结果"""
        result = StructureSortResult(
            success=True,
            structure_type="json",
            sort_order="ascending",
            original_input="test",
            extracted_content={"test": "data"},
            sorted_content=[{"id": 1}, {"id": 2}],
            formatted_output="formatted",
            processing_time=1.5,
            error_message=None,
            extraction_stats={"total_items": 2}
        )
        
        self.assertTrue(result.success)
        self.assertEqual(result.structure_type, "json")
        self.assertEqual(result.sort_order, "ascending")
        self.assertEqual(result.original_input, "test")
        self.assertEqual(result.extracted_content, {"test": "data"})
        self.assertEqual(len(result.sorted_content), 2)
        self.assertEqual(result.formatted_output, "formatted")
        self.assertEqual(result.processing_time, 1.5)
        self.assertIsNone(result.error_message)
        self.assertEqual(result.extraction_stats["total_items"], 2)
    
    @patch('lightce.tools.structure_sort.UniversalAgent')
    def test_structure_sort_agent_initialization(self, mock_agent_class):
        """测试结构化排序代理初始化"""
        # 模拟UniversalAgent
        mock_agent = MagicMock()
        mock_agent_class.return_value = mock_agent
        
        config = StructureSortConfig()
        agent = StructureSortAgent(config)
        
        self.assertEqual(agent.config, config)
        self.assertEqual(agent.processing_history, [])
        mock_agent_class.assert_called_once()
    
    @patch('lightce.tools.structure_sort.UniversalAgent')
    def test_create_structure_sort_agent(self, mock_agent_class):
        """测试创建结构化排序代理的便捷函数"""
        # 模拟UniversalAgent
        mock_agent = MagicMock()
        mock_agent_class.return_value = mock_agent
        
        agent = create_structure_sort_agent("json", "ascending", "gpt-3.5-turbo", 0.1)
        
        self.assertIsInstance(agent, StructureSortAgent)
        self.assertEqual(agent.config.structure_type, StructureType.JSON)
        self.assertEqual(agent.config.sort_order, SortOrder.ASCENDING)
        self.assertIsNotNone(agent.config.model_config)
        self.assertEqual(agent.config.model_config.model_name, "gpt-3.5-turbo")
        self.assertEqual(agent.config.model_config.temperature, 0.1)
    
    @patch('lightce.tools.structure_sort.UniversalAgent')
    def test_process_structure_with_agent(self, mock_agent_class):
        """测试使用代理进行结构化处理的便捷函数"""
        # 模拟UniversalAgent和处理结果
        mock_agent = MagicMock()
        mock_agent_class.return_value = mock_agent
        
        mock_result = StructureSortResult(
            success=True,
            structure_type="json",
            sort_order="ascending",
            original_input="test",
            extracted_content={"test": "data"},
            sorted_content=[{"id": 1}],
            formatted_output="formatted",
            processing_time=1.0,
            error_message=None,
            extraction_stats={"total_items": 1}
        )
        
        mock_agent.process_structure.return_value = mock_result
        
        result = process_structure_with_agent(self.test_json, "json", "ascending")
        
        self.assertTrue(result["success"])
        self.assertEqual(result["structure_type"], "json")
        self.assertEqual(result["sort_order"], "ascending")
        self.assertEqual(result["extraction_stats"]["total_items"], 1)
    
    def test_build_extraction_prompt(self):
        """测试构建提取提示词"""
        agent = StructureSortAgent()
        
        # 测试JSON提示词
        agent.config.structure_type = StructureType.JSON
        prompt = agent._build_extraction_prompt(self.test_json)
        self.assertIn("JSON数据", prompt)
        self.assertIn("完整提取所有字段和值", prompt)
        
        # 测试XML提示词
        agent.config.structure_type = StructureType.XML
        prompt = agent._build_extraction_prompt(self.test_xml)
        self.assertIn("XML数据", prompt)
        self.assertIn("提取所有XML标签和属性", prompt)
        
        # 测试CSV提示词
        agent.config.structure_type = StructureType.CSV
        prompt = agent._build_extraction_prompt(self.test_csv)
        self.assertIn("CSV数据", prompt)
        self.assertIn("解析CSV格式数据", prompt)
        
        # 测试表格提示词
        agent.config.structure_type = StructureType.TABLE
        prompt = agent._build_extraction_prompt("test table")
        self.assertIn("表格数据", prompt)
        self.assertIn("识别表格结构", prompt)
        
        # 测试列表提示词
        agent.config.structure_type = StructureType.LIST
        prompt = agent._build_extraction_prompt("test list")
        self.assertIn("列表数据", prompt)
        self.assertIn("识别列表项", prompt)
        
        # 测试树形提示词
        agent.config.structure_type = StructureType.TREE
        prompt = agent._build_extraction_prompt("test tree")
        self.assertIn("树形数据", prompt)
        self.assertIn("识别树形结构", prompt)
        
        # 测试图提示词
        agent.config.structure_type = StructureType.GRAPH
        prompt = agent._build_extraction_prompt("test graph")
        self.assertIn("图数据", prompt)
        self.assertIn("识别节点和边", prompt)
    
    def test_parse_structured_response(self):
        """测试解析结构化响应"""
        agent = StructureSortAgent()
        
        # 测试JSON响应
        json_response = '{"test": "data"}'
        result = agent._parse_structured_response(json_response)
        self.assertEqual(result, {"test": "data"})
        
        # 测试列表响应
        list_response = '[{"id": 1}, {"id": 2}]'
        result = agent._parse_structured_response(list_response)
        self.assertEqual(result, {"items": [{"id": 1}, {"id": 2}]})
        
        # 测试对象响应
        object_response = '{"items": [{"id": 1}]}'
        result = agent._parse_structured_response(object_response)
        self.assertEqual(result, {"items": [{"id": 1}]})
        
        # 测试非结构化响应
        raw_response = "This is a raw response"
        result = agent._parse_structured_response(raw_response)
        self.assertEqual(result, {"raw_content": raw_response, "parsed": False})
    
    def test_sort_content(self):
        """测试内容排序"""
        agent = StructureSortAgent()
        
        # 测试升序排序
        agent.config.sort_order = SortOrder.ASCENDING
        content = {"items": [{"id": 3}, {"id": 1}, {"id": 2}]}
        sorted_content = agent._sort_content(content, "id")
        self.assertEqual(sorted_content[0]["id"], 1)
        self.assertEqual(sorted_content[1]["id"], 2)
        self.assertEqual(sorted_content[2]["id"], 3)
        
        # 测试降序排序
        agent.config.sort_order = SortOrder.DESCENDING
        sorted_content = agent._sort_content(content, "id")
        self.assertEqual(sorted_content[0]["id"], 3)
        self.assertEqual(sorted_content[1]["id"], 2)
        self.assertEqual(sorted_content[2]["id"], 1)
        
        # 测试字母排序
        agent.config.sort_order = SortOrder.ALPHABETICAL
        content = {"items": [{"name": "张三"}, {"name": "李四"}, {"name": "王五"}]}
        sorted_content = agent._sort_content(content, "name")
        self.assertEqual(sorted_content[0]["name"], "李四")
        self.assertEqual(sorted_content[1]["name"], "王五")
        self.assertEqual(sorted_content[2]["name"], "张三")
        
        # 测试数值排序
        agent.config.sort_order = SortOrder.NUMERICAL
        content = {"items": [{"age": "28"}, {"age": "25"}, {"age": "32"}]}
        sorted_content = agent._sort_content(content, "age")
        self.assertEqual(sorted_content[0]["age"], "25")
        self.assertEqual(sorted_content[1]["age"], "28")
        self.assertEqual(sorted_content[2]["age"], "32")
        
        # 测试优先级排序
        agent.config.sort_order = SortOrder.PRIORITY
        content = {"items": [{"priority": "low"}, {"priority": "high"}, {"priority": "medium"}]}
        sorted_content = agent._sort_content(content, "priority")
        self.assertEqual(sorted_content[0]["priority"], "high")
        self.assertEqual(sorted_content[1]["priority"], "medium")
        self.assertEqual(sorted_content[2]["priority"], "low")
    
    def test_flatten_content(self):
        """测试内容扁平化"""
        agent = StructureSortAgent()
        
        # 测试列表扁平化
        content = [{"id": 1}, {"id": 2}]
        flattened = agent._flatten_content(content)
        self.assertEqual(flattened, content)
        
        # 测试字典扁平化
        content = {"a": {"id": 1}, "b": {"id": 2}}
        flattened = agent._flatten_content(content)
        self.assertEqual(flattened, [{"id": 1}, {"id": 2}])
        
        # 测试其他类型扁平化
        content = "test"
        flattened = agent._flatten_content(content)
        self.assertEqual(flattened, ["test"])
    
    def test_get_sort_value(self):
        """测试获取排序值"""
        agent = StructureSortAgent()
        
        # 测试字典排序值
        item = {"id": 1, "name": "test"}
        value = agent._get_sort_value(item, "id")
        self.assertEqual(value, 1)
        
        # 测试字符串排序值
        item = "test"
        value = agent._get_sort_value(item)
        self.assertEqual(value, "test")
        
        # 测试数字排序值
        item = 123
        value = agent._get_sort_value(item)
        self.assertEqual(value, 123)
        
        # 测试缺失键
        item = {"name": "test"}
        value = agent._get_sort_value(item, "id")
        self.assertEqual(value, "")
    
    def test_get_numerical_value(self):
        """测试获取数值用于排序"""
        agent = StructureSortAgent()
        
        # 测试整数
        value = agent._get_numerical_value({"age": 25}, "age")
        self.assertEqual(value, 25.0)
        
        # 测试浮点数
        value = agent._get_numerical_value({"price": 99.99}, "price")
        self.assertEqual(value, 99.99)
        
        # 测试字符串中的数字
        value = agent._get_numerical_value({"text": "价格100元"}, "text")
        self.assertEqual(value, 100.0)
        
        # 测试无数字的字符串
        value = agent._get_numerical_value({"text": "无数字"}, "text")
        self.assertEqual(value, 0.0)
    
    def test_get_chronological_value(self):
        """测试获取时间值用于排序"""
        agent = StructureSortAgent()
        
        # 测试标准日期格式
        value = agent._get_chronological_value({"date": "2024-01-15"}, "date")
        self.assertEqual(value, "2024-01-15")
        
        # 测试中文日期格式
        value = agent._get_chronological_value({"date": "2024年1月15日"}, "date")
        self.assertEqual(value, "2024年1月15日")
        
        # 测试无日期的字符串
        value = agent._get_chronological_value({"text": "无日期"}, "text")
        self.assertEqual(value, "无日期")
    
    def test_get_priority_value(self):
        """测试获取优先级值用于排序"""
        agent = StructureSortAgent()
        
        # 测试高优先级
        value = agent._get_priority_value({"priority": "high"}, "priority")
        self.assertEqual(value, 3)
        
        # 测试中优先级
        value = agent._get_priority_value({"priority": "medium"}, "priority")
        self.assertEqual(value, 2)
        
        # 测试低优先级
        value = agent._get_priority_value({"priority": "low"}, "priority")
        self.assertEqual(value, 1)
        
        # 测试无优先级
        value = agent._get_priority_value({"text": "无优先级"}, "text")
        self.assertEqual(value, 0)
    
    def test_format_output(self):
        """测试格式化输出"""
        agent = StructureSortAgent()
        
        test_content = [{"id": 1, "name": "张三"}, {"id": 2, "name": "李四"}]
        
        # 测试JSON格式化
        agent.config.structure_type = StructureType.JSON
        output = agent._format_output(test_content)
        self.assertIn('"id": 1', output)
        self.assertIn('"name": "张三"', output)
        
        # 测试XML格式化
        agent.config.structure_type = StructureType.XML
        output = agent._format_output(test_content)
        self.assertIn('<?xml version="1.0" encoding="UTF-8"?>', output)
        self.assertIn('<item id="0">', output)
        
        # 测试CSV格式化
        agent.config.structure_type = StructureType.CSV
        output = agent._format_output(test_content)
        self.assertIn('id,name', output)
        self.assertIn('1,张三', output)
        
        # 测试表格格式化
        agent.config.structure_type = StructureType.TABLE
        output = agent._format_output(test_content)
        self.assertIn('| id | name |', output)
        self.assertIn('| 1  | 张三 |', output)
        
        # 测试列表格式化
        agent.config.structure_type = StructureType.LIST
        output = agent._format_output(test_content)
        self.assertIn('- ', output)
        
        # 测试树形格式化
        agent.config.structure_type = StructureType.TREE
        output = agent._format_output(test_content)
        self.assertIn('├─', output)
        
        # 测试图格式化
        agent.config.structure_type = StructureType.GRAPH
        output = agent._format_output(test_content)
        self.assertIn('digraph G {', output)
    
    def test_format_as_xml(self):
        """测试XML格式化"""
        agent = StructureSortAgent()
        
        content = [{"id": 1, "name": "张三"}, {"id": 2, "name": "李四"}]
        xml_output = agent._format_as_xml(content)
        
        self.assertIn('<?xml version="1.0" encoding="UTF-8"?>', xml_output)
        self.assertIn('<root>', xml_output)
        self.assertIn('<item id="0">', xml_output)
        self.assertIn('<id>1</id>', xml_output)
        self.assertIn('<name>张三</name>', xml_output)
        self.assertIn('</root>', xml_output)
    
    def test_format_as_csv(self):
        """测试CSV格式化"""
        agent = StructureSortAgent()
        
        # 测试字典列表
        content = [{"id": 1, "name": "张三"}, {"id": 2, "name": "李四"}]
        csv_output = agent._format_as_csv(content)
        
        self.assertIn('id,name', csv_output)
        self.assertIn('1,张三', csv_output)
        self.assertIn('2,李四', csv_output)
        
        # 测试简单列表
        content = ["项目A", "项目B", "项目C"]
        csv_output = agent._format_as_csv(content)
        
        self.assertIn('项目A', csv_output)
        self.assertIn('项目B', csv_output)
        self.assertIn('项目C', csv_output)
    
    def test_format_as_table(self):
        """测试表格格式化"""
        agent = StructureSortAgent()
        
        content = [{"id": 1, "name": "张三"}, {"id": 2, "name": "李四"}]
        table_output = agent._format_as_table(content)
        
        self.assertIn('| id | name |', table_output)
        self.assertIn('| 1  | 张三 |', table_output)
        self.assertIn('| 2  | 李四 |', table_output)
        self.assertIn('|---|------|', table_output)
    
    def test_format_as_list(self):
        """测试列表格式化"""
        agent = StructureSortAgent()
        
        content = ["项目A", "项目B", "项目C"]
        list_output = agent._format_as_list(content)
        
        self.assertIn('- 项目A', list_output)
        self.assertIn('- 项目B', list_output)
        self.assertIn('- 项目C', list_output)
    
    def test_format_as_tree(self):
        """测试树形格式化"""
        agent = StructureSortAgent()
        
        content = [{"name": "张三", "children": [{"name": "子项目1"}]}]
        tree_output = agent._format_as_tree(content)
        
        self.assertIn('├─', tree_output)
        self.assertIn('└─', tree_output)
    
    def test_format_as_graph(self):
        """测试图格式化"""
        agent = StructureSortAgent()
        
        content = [{"name": "节点A", "connections": ["节点B"]}]
        graph_output = agent._format_as_graph(content)
        
        self.assertIn('digraph G {', graph_output)
        self.assertIn('node_0 [label="节点A"];', graph_output)
        self.assertIn('node_0 -> 节点B;', graph_output)
        self.assertIn('}', graph_output)
    
    def test_calculate_stats(self):
        """测试统计信息计算"""
        agent = StructureSortAgent()
        
        extracted_content = {"test": "data"}
        sorted_content = [{"id": 1, "name": "张三"}, {"id": 2, "name": "李四"}]
        
        stats = agent._calculate_stats(extracted_content, sorted_content)
        
        self.assertEqual(stats["total_items"], 2)
        self.assertTrue(stats["extraction_success"])
        self.assertTrue(stats["sorting_applied"])
        self.assertTrue(stats["formatting_applied"])
        self.assertIn("dict", stats["type_distribution"])
        self.assertEqual(stats["type_distribution"]["dict"], 2)
    
    @patch('lightce.tools.structure_sort.UniversalAgent')
    def test_batch_process(self, mock_agent_class):
        """测试批量处理"""
        # 模拟UniversalAgent
        mock_agent = MagicMock()
        mock_agent_class.return_value = mock_agent
        
        mock_result = StructureSortResult(
            success=True,
            structure_type="json",
            sort_order="ascending",
            original_input="test",
            extracted_content={"test": "data"},
            sorted_content=[{"id": 1}],
            formatted_output="formatted",
            processing_time=1.0,
            error_message=None,
            extraction_stats={"total_items": 1}
        )
        
        mock_agent.process_structure.return_value = mock_result
        
        agent = StructureSortAgent()
        input_data_list = ["data1", "data2", "data3"]
        custom_sort_keys = ["id", "name", "age"]
        
        results = agent.batch_process(input_data_list, custom_sort_keys)
        
        self.assertEqual(len(results), 3)
        for result in results:
            self.assertTrue(result.success)
            self.assertEqual(result.structure_type, "json")
            self.assertEqual(result.processing_time, 1.0)
    
    @patch('lightce.tools.structure_sort.UniversalAgent')
    def test_statistics(self, mock_agent_class):
        """测试统计信息"""
        # 模拟UniversalAgent
        mock_agent = MagicMock()
        mock_agent_class.return_value = mock_agent
        
        mock_result = StructureSortResult(
            success=True,
            structure_type="json",
            sort_order="ascending",
            original_input="test",
            extracted_content={"test": "data"},
            sorted_content=[{"id": 1}],
            formatted_output="formatted",
            processing_time=1.0,
            error_message=None,
            extraction_stats={"total_items": 1}
        )
        
        mock_agent.process_structure.return_value = mock_result
        
        agent = StructureSortAgent()
        
        # 执行多次处理
        for _ in range(3):
            agent.process_structure(self.test_json)
        
        stats = agent.get_statistics()
        
        self.assertEqual(stats["total_processings"], 3)
        self.assertEqual(stats["successful_processings"], 3)
        self.assertEqual(stats["success_rate"], 1.0)
        self.assertEqual(stats["average_processing_time"], 1.0)
        self.assertIn("json", stats["type_statistics"])
    
    def test_structure_sort_tool(self):
        """测试LangChain工具包装器"""
        # 创建模拟代理
        mock_agent = MagicMock()
        mock_result = StructureSortResult(
            success=True,
            structure_type="json",
            sort_order="ascending",
            original_input="test",
            extracted_content={"test": "data"},
            sorted_content=[{"id": 1}],
            formatted_output="formatted",
            processing_time=1.0,
            error_message=None,
            extraction_stats={"total_items": 1}
        )
        mock_agent.process_structure.return_value = mock_result
        
        # 创建工具
        tool = StructureSortTool(mock_agent)
        
        self.assertEqual(tool.name, "structure_sort")
        self.assertIn("结构化输入", tool.description)
        
        # 测试工具执行
        result = tool._run(self.test_json, "json", "ascending", "id")
        
        self.assertTrue(result["success"])
        self.assertEqual(result["structure_type"], "json")
        self.assertEqual(result["sort_order"], "ascending")
        self.assertEqual(result["processing_time"], 1.0)
    
    def test_error_handling(self):
        """测试错误处理"""
        agent = StructureSortAgent()
        
        # 测试空输入
        result = agent.process_structure("")
        self.assertFalse(result.success)
        self.assertIsNotNone(result.error_message)
        
        # 测试无效结构类型
        with self.assertRaises(ValueError):
            agent.config.structure_type = "invalid_type"
    
    def test_configuration_validation(self):
        """测试配置验证"""
        # 测试有效的配置
        config = StructureSortConfig(
            structure_type=StructureType.JSON,
            sort_order=SortOrder.ASCENDING,
            enable_extraction=True,
            enable_sorting=True,
            enable_formatting=True
        )
        
        self.assertEqual(config.structure_type, StructureType.JSON)
        self.assertEqual(config.sort_order, SortOrder.ASCENDING)
        self.assertTrue(config.enable_extraction)
        self.assertTrue(config.enable_sorting)
        self.assertTrue(config.enable_formatting)
    
    def test_enum_values(self):
        """测试枚举值"""
        # 测试结构类型枚举
        self.assertEqual(StructureType.JSON.value, "json")
        self.assertEqual(StructureType.XML.value, "xml")
        self.assertEqual(StructureType.YAML.value, "yaml")
        self.assertEqual(StructureType.CSV.value, "csv")
        self.assertEqual(StructureType.TABLE.value, "table")
        self.assertEqual(StructureType.LIST.value, "list")
        self.assertEqual(StructureType.TREE.value, "tree")
        self.assertEqual(StructureType.GRAPH.value, "graph")
        
        # 测试排序顺序枚举
        self.assertEqual(SortOrder.ASCENDING.value, "ascending")
        self.assertEqual(SortOrder.DESCENDING.value, "descending")
        self.assertEqual(SortOrder.ALPHABETICAL.value, "alphabetical")
        self.assertEqual(SortOrder.NUMERICAL.value, "numerical")
        self.assertEqual(SortOrder.CHRONOLOGICAL.value, "chronological")
        self.assertEqual(SortOrder.PRIORITY.value, "priority")
        self.assertEqual(SortOrder.CUSTOM.value, "custom")

def run_quick_test():
    """运行快速测试"""
    print("运行结构化排序工具快速测试...")
    
    # 创建测试实例
    test = TestStructureSortTool()
    test.setUp()
    
    # 运行关键测试
    test_cases = [
        test.test_structure_sort_config,
        test.test_structure_sort_result,
        test.test_create_structure_sort_agent,
        test.test_build_extraction_prompt,
        test.test_parse_structured_response,
        test.test_sort_content,
        test.test_flatten_content,
        test.test_get_sort_value,
        test.test_get_numerical_value,
        test.test_get_chronological_value,
        test.test_get_priority_value,
        test.test_format_output,
        test.test_format_as_xml,
        test.test_format_as_csv,
        test.test_format_as_table,
        test.test_format_as_list,
        test.test_format_as_tree,
        test.test_format_as_graph,
        test.test_calculate_stats,
        test.test_structure_sort_tool,
        test.test_error_handling,
        test.test_configuration_validation,
        test.test_enum_values
    ]
    
    passed = 0
    total = len(test_cases)
    
    for test_case in test_cases:
        try:
            test_case()
            passed += 1
            print(f"✓ {test_case.__name__} 通过")
        except Exception as e:
            print(f"✗ {test_case.__name__} 失败: {e}")
    
    print(f"\n测试结果: {passed}/{total} 通过")
    return passed == total

if __name__ == "__main__":
    # 运行快速测试
    if run_quick_test():
        print("\n所有快速测试通过！")
        
        # 运行完整测试套件
        print("\n运行完整测试套件...")
        unittest.main(verbosity=2)
    else:
        print("\n快速测试失败，请检查代码！") 