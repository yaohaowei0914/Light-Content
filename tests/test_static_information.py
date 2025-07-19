#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
静态信息提取提示系统测试
验证不同级别和类型的静态信息提取功能
"""

import unittest
from unittest.mock import patch, MagicMock
from lightce.prompt.static_information import (
    InformationLevel, InformationType,
    get_information_prompt, get_all_information_prompts,
    get_information_workflow, get_level_description,
    create_basic_information, create_intermediate_information,
    create_advanced_information, create_expert_information
)

class TestStaticInformation(unittest.TestCase):
    """静态信息提取系统测试类"""
    
    def setUp(self):
        """测试前的准备工作"""
        self.test_text = """
        张三，男，1985年3月15日出生，身份证号：110101198503151234，
        联系电话：13812345678，邮箱：zhangsan@example.com，
        地址：北京市朝阳区建国路88号，邮编：100020，
        现任ABC公司技术部经理，月薪15000元。
        """
    
    def test_information_levels(self):
        """测试信息提取级别枚举"""
        self.assertEqual(len(InformationLevel), 4)
        self.assertIn(InformationLevel.BASIC, InformationLevel)
        self.assertIn(InformationLevel.INTERMEDIATE, InformationLevel)
        self.assertIn(InformationLevel.ADVANCED, InformationLevel)
        self.assertIn(InformationLevel.EXPERT, InformationLevel)
    
    def test_information_types(self):
        """测试信息提取类型枚举"""
        self.assertEqual(len(InformationType), 8)
        expected_types = [
            'contact', 'address', 'datetime', 'numeric',
            'personal', 'organization', 'document', 'structured'
        ]
        for expected_type in expected_types:
            self.assertIn(expected_type, [t.value for t in InformationType])
    
    def test_get_level_description(self):
        """测试级别描述获取"""
        for level in InformationLevel:
            description = get_level_description(level)
            self.assertIsInstance(description, str)
            self.assertGreater(len(description), 0)
    
    def test_basic_information_prompts(self):
        """测试基础级别信息提取提示词"""
        prompts = get_all_information_prompts(InformationLevel.BASIC, text=self.test_text)
        
        # 验证基础级别包含3种提取类型
        self.assertEqual(len(prompts), 3)
        self.assertIn('contact', prompts)
        self.assertIn('address', prompts)
        self.assertIn('datetime', prompts)
        
        # 验证每个提示词都包含测试文本
        for prompt in prompts.values():
            self.assertIn(self.test_text.strip(), prompt)
    
    def test_intermediate_information_prompts(self):
        """测试中级级别信息提取提示词"""
        prompts = get_all_information_prompts(InformationLevel.INTERMEDIATE, text=self.test_text)
        
        # 验证中级级别包含3种提取类型
        self.assertEqual(len(prompts), 3)
        self.assertIn('numeric', prompts)
        self.assertIn('personal', prompts)
        self.assertIn('organization', prompts)
        
        # 验证每个提示词都包含测试文本
        for prompt in prompts.values():
            self.assertIn(self.test_text.strip(), prompt)
    
    def test_advanced_information_prompts(self):
        """测试高级级别信息提取提示词"""
        prompts = get_all_information_prompts(InformationLevel.ADVANCED, text=self.test_text)
        
        # 验证高级级别包含2种提取类型
        self.assertEqual(len(prompts), 2)
        self.assertIn('document', prompts)
        self.assertIn('structured', prompts)
        
        # 验证每个提示词都包含测试文本
        for prompt in prompts.values():
            self.assertIn(self.test_text.strip(), prompt)
    
    def test_expert_information_prompts(self):
        """测试专家级别信息提取提示词"""
        prompts = get_all_information_prompts(InformationLevel.EXPERT, text=self.test_text)
        
        # 验证专家级别包含2种提取类型
        self.assertEqual(len(prompts), 2)
        self.assertIn('comprehensive_extraction', prompts)
        self.assertIn('information_validation', prompts)
        
        # 验证每个提示词都包含测试文本
        for prompt in prompts.values():
            self.assertIn(self.test_text.strip(), prompt)
    
    def test_get_information_prompt(self):
        """测试获取特定信息提取提示词"""
        # 测试基础级别的联系信息提取
        prompt = get_information_prompt(InformationLevel.BASIC, InformationType.CONTACT, text=self.test_text)
        self.assertIsInstance(prompt, str)
        self.assertIn(self.test_text.strip(), prompt)
        self.assertIn("联系信息提取专家", prompt)
        
        # 测试中级级别的个人信息提取
        prompt = get_information_prompt(InformationLevel.INTERMEDIATE, InformationType.PERSONAL, text=self.test_text)
        self.assertIsInstance(prompt, str)
        self.assertIn(self.test_text.strip(), prompt)
        self.assertIn("个人信息提取专家", prompt)
    
    def test_get_information_prompt_invalid_level(self):
        """测试无效级别的错误处理"""
        with self.assertRaises(ValueError):
            get_information_prompt("invalid_level", InformationType.CONTACT, text=self.test_text)
    
    def test_get_information_prompt_invalid_type(self):
        """测试无效类型的错误处理"""
        with self.assertRaises(ValueError):
            get_information_prompt(InformationLevel.BASIC, "invalid_type", text=self.test_text)
    
    def test_get_information_workflow(self):
        """测试工作流获取"""
        for level in InformationLevel:
            workflow = get_information_workflow(level, self.test_text)
            
            # 验证工作流结构
            self.assertIn('level', workflow)
            self.assertIn('level_description', workflow)
            self.assertIn('input_text_length', workflow)
            self.assertIn('workflow_steps', workflow)
            self.assertIn('prompts', workflow)
            
            # 验证数据类型
            self.assertIsInstance(workflow['level'], str)
            self.assertIsInstance(workflow['level_description'], str)
            self.assertIsInstance(workflow['input_text_length'], int)
            self.assertIsInstance(workflow['workflow_steps'], list)
            self.assertIsInstance(workflow['prompts'], dict)
            
            # 验证工作流步骤不为空
            self.assertGreater(len(workflow['workflow_steps']), 0)
            
            # 验证提示词不为空
            self.assertGreater(len(workflow['prompts']), 0)
    
    def test_convenience_functions(self):
        """测试便捷函数"""
        # 测试基础级别便捷函数
        basic_prompts = create_basic_information(self.test_text)
        self.assertEqual(len(basic_prompts), 3)
        self.assertIn('contact', basic_prompts)
        
        # 测试中级级别便捷函数
        intermediate_prompts = create_intermediate_information(self.test_text)
        self.assertEqual(len(intermediate_prompts), 3)
        self.assertIn('personal', intermediate_prompts)
        
        # 测试高级级别便捷函数
        advanced_prompts = create_advanced_information(self.test_text)
        self.assertEqual(len(advanced_prompts), 2)
        self.assertIn('document', advanced_prompts)
        
        # 测试专家级别便捷函数
        expert_prompts = create_expert_information(self.test_text)
        self.assertEqual(len(expert_prompts), 2)
        self.assertIn('comprehensive_extraction', expert_prompts)
    
    def test_prompt_formatting(self):
        """测试提示词格式化"""
        # 测试包含多个参数的提示词格式化
        custom_text = "这是一个测试文本"
        custom_param = "自定义参数"
        
        prompt = get_information_prompt(
            InformationLevel.BASIC, 
            InformationType.CONTACT, 
            text=custom_text,
            custom_param=custom_param
        )
        
        self.assertIn(custom_text, prompt)
    
    def test_workflow_step_counts(self):
        """测试不同级别的工作流步骤数量"""
        expected_steps = {
            InformationLevel.BASIC: 3,
            InformationLevel.INTERMEDIATE: 3,
            InformationLevel.ADVANCED: 3,
            InformationLevel.EXPERT: 3
        }
        
        for level, expected_count in expected_steps.items():
            workflow = get_information_workflow(level, self.test_text)
            self.assertEqual(len(workflow['workflow_steps']), expected_count)
    
    def test_prompt_content_quality(self):
        """测试提示词内容质量"""
        for level in InformationLevel:
            prompts = get_all_information_prompts(level, text=self.test_text)
            
            for information_type, prompt in prompts.items():
                # 验证提示词包含必要的元素
                self.assertIn("你是一个", prompt)  # 角色定义
                self.assertIn("请", prompt)  # 指令性语言
                self.assertIn(self.test_text.strip(), prompt)  # 输入文本
                
                # 验证提示词长度合理
                self.assertGreater(len(prompt), 100)  # 提示词应该足够详细
                self.assertLess(len(prompt), 5000)  # 提示词不应该过长
    
    def test_specific_information_extraction(self):
        """测试特定信息类型的提取"""
        # 测试联系信息提取
        contact_prompt = get_information_prompt(
            InformationLevel.BASIC, 
            InformationType.CONTACT, 
            text=self.test_text
        )
        self.assertIn("电话号码", contact_prompt)
        self.assertIn("邮箱地址", contact_prompt)
        
        # 测试个人信息提取
        personal_prompt = get_information_prompt(
            InformationLevel.INTERMEDIATE, 
            InformationType.PERSONAL, 
            text=self.test_text
        )
        self.assertIn("姓名", personal_prompt)
        self.assertIn("身份证号", personal_prompt)
        
        # 测试数字信息提取
        numeric_prompt = get_information_prompt(
            InformationLevel.INTERMEDIATE, 
            InformationType.NUMERIC, 
            text=self.test_text
        )
        self.assertIn("金额信息", numeric_prompt)
        self.assertIn("数量信息", numeric_prompt)

def run_quick_test():
    """运行快速测试"""
    print("运行静态信息提取系统快速测试...")
    
    # 创建测试实例
    test = TestStaticInformation()
    test.setUp()
    
    # 运行关键测试
    test_cases = [
        test.test_information_levels,
        test.test_information_types,
        test.test_basic_information_prompts,
        test.test_intermediate_information_prompts,
        test.test_advanced_information_prompts,
        test.test_expert_information_prompts,
        test.test_get_information_workflow,
        test.test_convenience_functions
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